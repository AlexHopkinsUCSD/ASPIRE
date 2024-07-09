from pydantic import BaseModel
from typing import Optional

class ConfigSettings(BaseModel):
    OIDC_AUTH_REQ_URL: str
    OIDC_AUTH_REDIRECT_URI: str
    OIDC_INITIATION_URL: str
    OIDC_TARGET_LINK_URI: str
    PUBLIC_JWK_URL: str
    DOMAIN_NAME: str
    PLATFORM_ISS: str
    WEB_APP_TITLE: str
    WEB_APP_DESCRIPTION: str
    PUBLIC_JWK_URL: str
    LTI_PUBLIC_KEY: Optional[str]
    LTI_PRIVATE_KEY: Optional[str]