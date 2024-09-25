from typing import List, Optional, Protocol, Set


from fastapi_lti1p3 import Session


class DataAccessService(Protocol):
    """
    Provides the ids of various tables the client can access and their use permissions given their roles and tool context
    """
    async def accessible_modules(self, accepted_roles: Optional[Set[str]]) -> List[int]:
        ...

    async def accessible_student_knowledge(self, accepted_roles: Optional[Set[str]]) -> List[str]:
        ...
    
    async def authorized_data(self):
        ...