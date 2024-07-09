from typing import Protocol
from ..session_cache import Nonce

class LTI(Protocol):

    async def _create_nonce_session(self, iss, client_id, target_link_uri) -> Nonce:
        pass
    
    async def create_auth_response(
        self,
        iss, 
        login_hint, 
        target_link_uri,
        client_id,
        deployment_id,
        canvas_region,
        canvas_environment,
        redirect_uri: str
        ):
        pass

    async def validateResponse(state, id_token, public_jwk_url: str):
        pass