from pydantic import BaseModel
from typing import Optional, Literal, Union

class ClientCredentials(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int
    token_type: str
    user_id: Union[int, str]
    name: str
    global_id: Union[int, str]

class Session(BaseModel):
    #Primary Key
    session_id: str
    id_token: dict
    csrf_token: str
    client_credentials: Optional[ClientCredentials] = None
    client_id: Optional[str] = None

    def __eq__(self, other):
        if isinstance(other, Session):
            return self.session_id == other.session_id
        if isinstance(other, str):
            return self.session_id == other
        return NotImplemented
    
    def __hash__(self):
        return hash(self.session_id)

    def update(self, **kwargs):
        for field, value in kwargs.items():
            try:
                setattr(self, field, value)
            except ValueError:
                pass

        return self

    def __str__(self) -> str:
        return self.session_id
    
    def get_roles(self):
        return set(self.id_token.get("https://purl.imsglobal.org/spec/lti/claim/custom").get("roles").split(","))


class Nonce(BaseModel):
    #Primary Key
    nonce: str
    target_link_uri: str
    client_id: str
    state: str
    storage_target: Optional[str] = "cookie"

    def __eq__(self, other):
        if isinstance(other, Nonce):
            return self.nonce == other.nonce
        if isinstance(other, str):
            return self.nonce == other
        return NotImplemented
    
    def __hash__(self):
        return hash(self.nonce)
    
    def update(self, **kwargs):
        for field, value in kwargs.items():
            try:
                setattr(self, field, value)
            except ValueError:
                pass
            
        return self
    
    def __str__(self) -> str:
        return self.nonce


    