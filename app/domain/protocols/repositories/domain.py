from typing import List, Optional, Protocol, Union

from app.domain.models.domain import DomainRead, DomainCreate
from app.domain.models.errors import ErrorResponse

class DomainRepository(Protocol):
    async def add(self, domain: DomainCreate) -> Union[DomainRead, ErrorResponse]:
        ...