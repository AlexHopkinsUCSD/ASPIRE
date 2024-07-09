import logging

from typing import Union
from fastapi import Depends
from sqlmodel import Session

from app.infrastructure.database.db import get_db

from app.app.errors.db_error import DBError

from app.domain.protocols.repositories.domain import DomainRepository as DomainRepoProtocol

from app.domain.models.domain import DomainCreate, DomainRead, Domain
from app.domain.models.errors import ErrorResponse

logger = logging.getLogger(__name__)

class DomainRepository(DomainRepoProtocol):
    ''' 
    Provides data access to Domain models.
    '''
    
    db: Session
    
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    async def add(self, domain: DomainCreate) -> Union[DomainRead, ErrorResponse]:
        try:
            db_domain = Domain.from_orm(domain)
            self.db.add(db_domain)
            self.db.commit()
            self.db.refresh(db_domain)
            return DomainRead(**dict(db_domain))
        
        except Exception as e:
            logger.exception(msg="Failed to add Domain object.")
            raise DBError(
                origin="DomainRepository.add",
                type="QueryExecError",
                status_code=500,
                message="Failed to create domain"
            ) from e