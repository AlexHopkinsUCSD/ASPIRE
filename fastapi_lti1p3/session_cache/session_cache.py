from typing import Literal, Any, Union
from ..models.cache_models import Session, Nonce
from .data_store import DataStore

#TODO: Add option to Replace this cache with a Redis cache if the app scales beyond its capacity
#TODO: Create protocol for session cache
class SessionCache:
    """
    In memory data cache following the Singleton pattern, 
    contains two data stores: session_store and nonce_store

    session_store - storage for active client-sessions

    nonce_store - Temporary storage for nonce value and other lti launch params, used during oidc auth process
    """
    _cache = None

    def __new__(cls, *args, **kwargs):
        if not cls._cache:
            cls._cache = super(SessionCache, cls).__new__(cls, *args, **kwargs)
        return cls._cache
    
    def __init__(self) -> None:
        if not hasattr(self, "initialized"):
            self.session_store = DataStore()
            self.nonce_store = DataStore()
            self.initialized = True


    async def get(self, cache_id: str, store: Literal["session", "nonce"]) -> Union[Session, Nonce, None]:
        """
        Returns an object cached in one of the two data stores.
        
        :param cache_id: The key used to retrieve a cached Nonce or Session object
        :param store: The data store to search: The 'session' data store contains client sessions. The 'nonce' data store contains temporary data related to the oidc auth handshake. 

        ---
        WARNING: Nonce objects can only be retrieved ONCE before automatic deletion
        ---
        """
        if store == "session":
            return self.session_store[cache_id]
        else:
            nonce_session = self.nonce_store[cache_id]
            await self.delete(cache_id=cache_id, store="nonce")
            return nonce_session
    
    async def get_all(self, store: Literal["session", "nonce"]) -> dict:
        #TODO: Delete this method if unused in prod
        """
        Returns the entire cached dictionary of one of the two stores, only really used for debugging
        """
        if store == "session":
            return self.session_store._data
        else:
            return self.nonce_store._data

    async def create_cache(self, value: Union[Session, Nonce]) -> bool:
        """
        Creates a new cache, automatically determine which store to insert to based on the object type, session_id/nonce value must be unique.

        :param value: The new cached object, must be an instance of either a Session class with a unique session_id, or a Nonce class with a unique nonce value.
        :returns: Boolean value, True if value was successfully inserted, False if it was not.
        """
        if isinstance(value, Session):
            return await self.session_store.append(value)
        else:
            return await self.nonce_store.append(value)

    async def set(self, cache_id: str, key: str, value: Any, store: Literal["session", "nonce"]) -> Union[Session, Nonce, None]:
        """
        Used to set an attribute of a cached object

        :param cache_id: The key of the cached object being updated
        :param key: The attribute being set on the cached object
        :param value: The value being applied to the attribute
        :param store: The data store to search: The 'session' data store contains client sessions. The 'nonce' data store contains temporary data related to the oidc auth handshake. 
        :returns: The updated Session or Nonce object
        """
        if store == "session":
            self.session_store[cache_id] = {key: value}
            return self.session_store[cache_id]
        else:
            self.nonce_store[cache_id] = {key: value}
            return self.nonce_store[cache_id]


    async def delete(self, cache_id: str, store: Literal["session", "nonce"]) -> None:
        """
        Deletes a cached object, if no object exists at the cache_id and store does nothing.

        :param cache_id: The key of the cached object being deleted
        :param store: The data store to search: The 'session' data store contains client sessions. The 'nonce' data store contains temporary data related to the oidc auth handshake. 
        """
        if store == "session":
            del self.session_store[cache_id]
        else:
            del self.nonce_store[cache_id]