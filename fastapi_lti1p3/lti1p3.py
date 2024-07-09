import secrets

import uuid
import os

from fastapi import Request
from urllib.parse import urlencode

from .session_cache import SessionCache, Session, Nonce
from .protocols.lti1p3 import LTI as LTIProtocol
from .config import AdapterConfig
from .models.settings import ConfigSettings
from .auth_response_validator import AuthResponseValidator


class LTI(LTIProtocol):
    def __init__(self, request: Request):
        """
        Contains methods for handling the LTI1.3 launch process with FastAPI and generating persistent client-sessions
        :param request: A FastAPI request object, the content of this request object must be appropriate for method used during the various launch steps
        """
        self._settings: ConfigSettings = AdapterConfig().get_settings()
        self._private_key: str = os.environ.get("LTI_PRIVATE_KEY")
        self._request: Request = request
        self.session_cache = SessionCache()


    async def _create_nonce_session(self, client_id: str, target_link_uri: str, storage_target: str="cookie") -> tuple[Nonce, str]:
        """
        Generates a new nonce value and csrf token, caches them in a new nonce session, then returns the nonce object and csrf token

        :param client_id: The client_id field from the initiated login request, used to validate the request is coming from an accepted origin
        :param target_link_uri: The target_link_uri field from the initiated login request, used to set the final redirect
        """
        nonce = secrets.token_urlsafe(32)
        csrf = secrets.token_urlsafe(32)
        #TODO: Might be a risk of the nonce value becoming a duplicate of an existing one due to use of token_urlsafe instead of uuid4, 
        # since I need it to be both a shared secret and an identifier for the cache im not sure of the best approach. 
        # This is probably fine given 32 bit length and regular deletion of entries in the nonce_store after auth completion, if not a different approach is necessary
        self.session_cache.create_cache(
            value=Nonce(
                nonce=nonce, 
                target_link_uri=target_link_uri, 
                client_id=client_id, 
                state=csrf,
                storage_target=storage_target
            )
        )
        return nonce, csrf


    async def create_auth_response(self) -> str:
        """
        Used in steps 1 & 2 of the LTI1.3 launch process: 
        https://www.imsglobal.org/spec/security/v1p0/#step-1-third-party-initiated-login
        https://www.imsglobal.org/spec/security/v1p0/#step-2-authentication-request
        
        Takes the iss, login_hint, and target_link from the Third-party initiated login response from the lms platform,
        generates a nonce value and csrf token, stores them in a temporary nonce session,
        then packages an Authentication request with the appropriate query params, returning a url for the redirect.

        :returns: A url string with attached query params for the auth request redirect
        :rtype: str
        """
        init_token = await self._request.form()

        storage_target = "cookie"

        if not self._request.cookies and init_token.get("lti_storage_target"):
            #determines where the final session_id is to be stored dependent on 3rd-party cookie support
            storage_target = init_token.get("lti_storage_target")
            
        #TODO: validate client_id
        client_id = init_token.get("client_id")
        target_link_uri = init_token.get("target_link_uri")
        login_hint = init_token.get("login_hint")

        nonce, csrf = await self._create_nonce_session(client_id=client_id, target_link_uri=target_link_uri, storage_target=storage_target)

        params = {
            "response_type": "id_token", 
            "response_mode": "form_post",
            "client_id": client_id, 
            "redirect_uri": f"{self._settings.DOMAIN_NAME}{self._settings.OIDC_AUTH_REDIRECT_URI}",
            "nonce": nonce,
            "state": csrf,
            "scope": "openid",
            "login_hint": login_hint,
            "prompt": None
            }

        auth_req_url = f"{self._settings.OIDC_AUTH_REQ_URL}?{urlencode(params)}"

        return auth_req_url


    async def validateResponse(self) -> tuple[str, str, str, str]:
        """
        Validates the platforms auth response, if no errors are raised, creates a new client-session and returns the uuid of that session and a new csrf token. 

        Used in step 3 of the LTI1.3 launch process: 
        https://www.imsglobal.org/spec/security/v1p0/#step-3-authentication-response
    
        :returns: (session_id, csrf token, target_link_uri)
        :rtype: tuple
        :raises TokenValidationError: If the token is invalid, the message attribute contains the cause and the status_code attribute contains the recommended http response status code
        """
        auth_validator = AuthResponseValidator(request=self._request)
        
        validated_token, target_link_uri, storage_target = await auth_validator.validate_token()
        # print(validated_token)
        session_id = uuid.uuid4().hex
        # print(session_id)
        csrf_token = secrets.token_urlsafe(32)

        #Create new client session
        new_session = Session(session_id=session_id, id_token=validated_token, csrf_token=csrf_token)
        self.session_cache.create_cache(new_session)

        return session_id, csrf_token, target_link_uri, storage_target, self._settings.OIDC_AUTH_REQ_URL
