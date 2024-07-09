from ..utils import generate_rsa_key_pair
from ..models.settings import ConfigSettings

class AdapterConfig:
    _config = None

    def __new__(cls, *args, **kwargs):
        if not cls._config:
            cls._config = super(AdapterConfig, cls).__new__(cls, *args, **kwargs)
        return cls._config
    
    def __init__(self) -> None:
        if not hasattr(self, "initialized"):
            self.initialized = True
            self._settings = None

    def assign_key_pair(self):
        private_pem, public_pem = generate_rsa_key_pair()
        self._settings.LTI_PRIVATE_KEY = private_pem.decode("utf-8")
        self._settings.LTI_PUBLIC_KEY = public_pem.decode("utf-8")

    def set_settings(self, settings: ConfigSettings):
        self._settings = settings

    def get_settings(self):
        return self._settings