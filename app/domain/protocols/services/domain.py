from typing import List, Optional, Protocol, Union

from app.domain.models.domain import DomainCreate, DomainRead
from app.domain.models.errors import ErrorResponse

class DomainService(Protocol):
    async def create_domain(self, domain: DomainCreate) -> Union[DomainRead, ErrorResponse]:
        ...

    async def get_module(self, domain_id: int) -> DomainRead:
        ...