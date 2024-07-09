from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseSettings


class Settings(BaseSettings):

    # Base required settings for FastAPI to function
    BASE_PATH: str # For EKS deployment, this path is very important. It defines at what path the API will be available from the root url (e.g. namespace.ucsd.edu/BASE_PATH)
    WEB_APP_DEBUG: bool
    WEB_APP_DESCRIPTION: str
    WEB_APP_TITLE: str
    WEB_APP_VERSION: str
    
    # TODO Define required settings, including environment variables. Samples below.
    ENV: str
    LOG_LEVEL: str
    SSO_SP_ENTITY_ID: str
    SSO_REDIS_SESSION_PREFIX: str
    REDIS_URL: str
    DATABASE1_URL: str
    APIM_TOKEN_URL: str
    APIM_BASE_URL: str
    APIM_CLIENT_KEY: str
    APIM_SECRET_KEY: str
    OIDC_AUTH_REQ_URL: str
    OIDC_AUTH_REDIRECT_URI: str
    OIDC_INITIATION_URL: str
    OIDC_TARGET_LINK_URI: str
    PUBLIC_JWK_URL: str
    DOMAIN_NAME: str
    PLATFORM_ISS: str
    WEB_APP_TITLE: str
    WEB_APP_DESCRIPTION: str
    
@lru_cache # Cache settings
def get_settings() -> Settings:
    load_dotenv()
    settings = Settings()
    return settings
