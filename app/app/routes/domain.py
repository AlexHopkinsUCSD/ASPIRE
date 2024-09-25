from http.client import HTTPException
from typing import Optional, List, Union
from app.domain.models.domain import DomainRead
from app.domain.models.errors import ErrorResponse
from app.domain.services.domain import DomainService 
from app.domain.protocols.services.domain import DomainService as DomainServiceProtocol
from ..errors.db_error import DBError

from fastapi import APIRouter, Depends, Form, HTTPException, Response, Request

from fastapi_lti1p3 import enforce_auth

from app.domain.models.domain import DomainUpdate
from app.domain.services.data_access import DataAccessService
from app.domain.protocols.services.data_access import DataAccessService as DataAccessServiceProtocol

router = APIRouter()


delete_me = [
    {
        "object": "edge",
        "action": "delete",
        "value": {
            "target": "concept_4_module_1",
            "source": "concept_x2_module_1_and_2"
        }
    },
    {
        "object": "edge",
        "action": "add",
        "value": {
            "source": "concept_2_module_2",
            "target": "concept_4_module_1"
        }
    },
    {
        "object": "node",
        "action": "delete",
        "value": {
            "subject": "computer science",
            "difficulty": 1,
            "name": "concept_x2_module_1_and_2",
            "id": "concept_x2_module_1_and_2",
            "module": [
                1,
                2
            ],
            "params": {
                "focusColor": "#f55d42"
            }
        }
    },
    {
        "object": "node",
        "action": "add",
        "value": {
            "name": "test add concept",
            "id": "test add concept",
            "module": [
                1
            ]
        }
    },
    {
        "object": "nodeToModule",
        "action": "add",
        "value": {
            "nodeIds": [
                "test add concept"
            ],
            "module": 1
        }
    },
    {
        "object": "nodeToModule",
        "action": "delete",
        "value": {
            "nodeIds": [
                "concept_4_module_1"
            ],
            "module": 1
        }
    }
]

#Routes related to the Domain and Domain structure 
@router.put("", name="domain:update-domain")
async def update_domain(
    request: Request,
    change_history: List[DomainUpdate],
    # data_access: DataAccessServiceProtocol = Depends(
    #     DataAccessService(
    #         accepted_roles={"DesignerEnrollment", "TeacherEnrollment"},
    #         data_targets=["module_access", "course_access", "student_access"]
    #         )
    #     )
    ):
    """
    Updates a domain model to match changes supplied by 'change_history', client must have appropriate data access to modify the domain model
    """
    print(change_history)
    


@router.get("/get/{domain_id}/domain", name="Domain:get-domain", response_model=Union[DomainRead, ErrorResponse])
async def get_domain(
    request: Request, 
    response: Response,
    domain_id: int,
    domain_service: DomainServiceProtocol = Depends(DomainService)
    ) -> Union[DomainRead, ErrorResponse]:
    """
    Returns a single domain by its domain_id
    """
    try:
        return await domain_service.get_domain(domain_id=domain_id)
    
    except DBError as e:
        response.status_code = e.status_code
        return ErrorResponse(
            code=e.status_code,
            type=e.type,
            message=str(e)
        )