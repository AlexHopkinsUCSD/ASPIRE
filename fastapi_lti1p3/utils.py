import requests

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

from .models.settings import ConfigSettings

def generate_rsa_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    return private_pem, public_pem

async def get_developer_key_json(tool_public_jwk_url: str, _settings: ConfigSettings):
    dev_key = {
        "title": _settings.WEB_APP_TITLE,
        "description": _settings.WEB_APP_DESCRIPTION,
        "oidc_initiation_url": _settings.OIDC_INITIATION_URL,
        "target_link_uri": _settings.OIDC_TARGET_LINK_URI,
        "public_jwk_url": tool_public_jwk_url,
        "extensions": [
            {
                "domain": "ASPIRE-App",
                "tool_id": "dawds32656",
                "platform": "canvas.instructure.com",
                "privacy_level": "public",
                "selection_height": 800,
                "selection_width": 800,
                "placements": [
                {
                    "text": "User Navigation Placement",
                    "placement": "user_navigation",
                    "message_type": "LtiResourceLinkRequest",
                    "target_link_uri": "https://your.target_link_uri/my_dashboard",
                    "canvas_icon_class": "icon-lti",
                    "custom_fields": {
                    "foo": "$Canvas.user.id"
                    }
                }
                ]
            }
        ]
    }
    return dev_key


async def get_platform_public_key(settings: ConfigSettings):
    platform_key = requests.get(url=settings.PUBLIC_JWK_URL).json()
    return platform_key


async def get_tool_public_key(settings: ConfigSettings):
    jwk = {
        "public_jwk": {
            "kty": "RSA",
            "alg": "RS256",
            "e": "AQAB",
            "kid": "aksdjhkuahdlkahj-adaldhakihdad46ad432%",
            "n": settings.LTI_PUBLIC_KEY,
            "use": "sig"
        }   
    }
    return jwk