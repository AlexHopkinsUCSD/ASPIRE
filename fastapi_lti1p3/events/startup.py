from ..config import AdapterConfig
from ..models.settings import ConfigSettings

def init_adapter_config(settings: ConfigSettings):
    adapter_config = AdapterConfig()
    adapter_config.set_settings(settings=settings)
    adapter_config.assign_key_pair()

# async def lti_startup_events():
#     await assign_key_pair()