from pydantic import BaseModel
from typing import Optional, Literal

class Session(BaseModel):
    #Primary Key
    session_id: str
    id_token: dict
    csrf_token: str

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

class Nonce(BaseModel):
    #Primary Key
    nonce: str
    target_link_uri: str
    client_id: int
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


    