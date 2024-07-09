from typing import List, Optional, Union
from fastapi import Depends, UploadFile

from app.domain.protocols.repositories.domain import DomainRepository as DomainRepoProtocol
from app.domain.protocols.services.domain import DomainService as DomainServiceProtocol
from app.infrastructure.database.repositories.domain import DomainRepository
from app.domain.models.domain import DomainCreate, DomainRead
from app.domain.models.errors import ErrorResponse


class DomainService(DomainServiceProtocol):
    def __init__(
            self, 
            domain_repo: DomainRepoProtocol = Depends(DomainRepository)
    ):
        self.domain_repo = domain_repo

    async def create_domain(self, domain: DomainCreate) -> Union[DomainRead, ErrorResponse]:
        return await self.domain_repo.add(domain)
