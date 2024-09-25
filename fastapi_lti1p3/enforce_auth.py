from .session_cache import SessionCache, Session
from .errors.validation_errors import AuthValidationError
from fastapi import Request

from typing import Set, Optional

async def enforce_auth(
        request: Request,
        cookie_name: str = "lti-session-id",
        header_name: str = "x-session-cookie",
        session_id: Optional[str]=None, 
        accepted_roles: Optional[Set[str]]=None
    ) -> Session:
    """
    Searches for a session_id in the cookies, headers, or session_id argument, 
    if one exists, it matches a session stored in the SessionCache, 
    and if the user assigned to that session contains any of the accepted roles, 
    returns the Session object of the client.

    :param request: REQUIRED - The request object of the protected endpoint. Must contain either a cookie or a header containing a valid session_id **EXCEPT** if overridden with the session_id arg.

    :param cookie_name: OPTIONAL - The key used to fetch the session cookie if one is provided, defaults to 'lti-session-id'.

    :param header_name: OPTIONAL - The key used to fetch the session header if one provided, defaults to 'x-session-cookie'.

    :param session_id: OPTIONAL - The id of the client session as generated and stored during the lti launch process.

    :param accepted_roles: OPTIONAL - A set of strings exactly matching at least one of the required user roles originating from the LMS platform, or None if all roles are acceptable.

    :returns Session: returned only if validation checks pass

    :raises AuthValidationError: If no session is found or session does not contain any of the accepted roles

    <hr/>

    =================
    Expose Headers
    =================
    
    In cases where cookies are blocked by 3rd party cookie policies, enforce_auth is equipped to search for the the session_id within a custom header specified by the 'header_name' arg. 
    In order to allow custom headers to attach to a FastAPI Request object, the specific header must be exposed using the built-in CORS Middleware.
    
    **below is an example of how to do this:**

```python

    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware

    app = FastAPI()
    # Add your custom headers to expose_header's list of strings
    app.add_middleware(CORSMiddleware, expose_headers=["x-session-cookie"])

```
    <br/>
    <hr/>

    =================
    Modify Role Check
    =================

    Roles are checked by first evoking the `Session.get_roles()` method, 
    by default this expects roles to exist on the id_token at the "https://purl.imsglobal.org/spec/lti/claim/custom" key as a comma separated string,
    then the result is checked against the conditional `if accepted_roles and not client_roles & accepted_roles:` 
    to determine either if all roles are acceptable or if roles have been specified and the result of `Session.get_roles()` is a subset/superset of the specified roles.

    Because Sessions can be overridden and/or the location where roles are stored may vary it is possible to modify the `Session.get_roles()` method at adapter configuration.

    **Here is an example override:**

```python
    from fastapi_lti1p3 import Session, ToolConfigSettings, init_adapter_config
    from irrelevant_to_example import platform_config
    from typing import List, Optional, Set
    # New model must extend 'Session'
    class ModifiedSession(Session):
        # Example adds an additional 'role' field to the Session class, the value will not be automatically added by the library on session creation,
        # therefore it must be set as Optional and/or with a default value, and added by the developer at a later stage.
        roles: Optional[List[str]]
        # Overrides the default get_roles() method
        def get_roles(self) -> Set[str]:
            # Must return a set of strings
            return set(self.roles)

    # Add new SESSION_CLASS to ToolConfigSettings and initialize.
    tool_config = ToolConfigSettings(**extra_tool_config, SESSION_CLASS=ModifiedSession)
    init_adapter_config(tool_settings=tool_config, platform_settings=platform_config)
```

    """

    if session_id:
        pass
    
    elif request.cookies.get(cookie_name):
        session_id = request.cookies.get(cookie_name)

    elif request.headers.get(header_name):
        session_id = request.headers.get(header_name)

    else:
        raise AuthValidationError(
            status_code=403, 
            message=f"session_id not found - session_id must be supplied in one of the following locations:\n1) In a cookie with a key == {cookie_name}\n2) In the headers with a key == {header_name}\n3) Supplied directly in the session_id argument"
            )
    
    cache = SessionCache()
    session_data = await cache.get(cache_id=session_id, store="session")

    # No session found
    if not session_data:
        raise AuthValidationError(status_code=401, message="Authentication Required")
    
    # accepted_roles not none and Insufficient permissions
    if accepted_roles and not session_data.get_roles() & accepted_roles:
        raise AuthValidationError(status_code=403, message="Insufficient Permissions")

    # Both checks pass, the user has authenticated and has valid permissions
    return session_data

    
