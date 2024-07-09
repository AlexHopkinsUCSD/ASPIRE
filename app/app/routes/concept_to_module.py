from http.client import HTTPException
from typing import Optional, List, Union

from fastapi import APIRouter, Depends, Form, HTTPException, Response, Request

from ..errors.db_error import DBError
from app.domain.models.errors import ErrorResponse

from app.domain.models.concept import ConceptCreate, ConceptCreateBulkRead, ConceptRead, ConceptToModuleCreate, ConceptToModuleDelete, ConceptToModuleRead, ConceptBulkRead
from app.domain.protocols.services.concept import ConceptToModuleService as CToMServiceProtocol
from app.domain.services.concept import ConceptService


router = APIRouter()

@router.post("", name="ConceptToModule:create-concept-to-module-junction", response_model=Union[List[ConceptToModuleRead], ErrorResponse])
async def create_cm_junction(
    request: Request, 
    response: Response,
    junctions: List[ConceptToModuleCreate],
    c_to_m_service: CToMServiceProtocol = Depends(ConceptService)
    ) -> Union[List[ConceptToModuleRead], ErrorResponse]:
    """
    Creates a new ConceptToModule Junction
    """
    try:
        return await c_to_m_service.bulk_create_module_junctions(junctions=junctions)

    except DBError as e:
        response.status_code = e.status_code
        return ErrorResponse(
            code=e.status_code,
            type=e.type,
            message=str(e)
        )

@router.get("/{module_id}", name="ConceptToModule:get-all-module-concepts", response_model=Union[ConceptBulkRead, ErrorResponse])
async def get_module_concepts(
    request: Request, 
    response: Response,
    module_id: int,
    c_to_m_service: CToMServiceProtocol = Depends(ConceptService)
    ) -> Union[ConceptBulkRead, ErrorResponse]:
    """
    Returns all concepts belonging to a module
    """
    try:
        return await c_to_m_service.get_all_concepts_in_module(module_id=module_id)

    except DBError as e:
        response.status_code = e.status_code
        return ErrorResponse(
            code=e.status_code,
            type=e.type,
            message=str(e)
        )

#TODO: Add return for success and failure to delete
@router.delete("", name="ConceptToModule:delete-concept-from-module")
async def delete_module_concept(
    request: Request, 
    response: Response,
    junctions: List[ConceptToModuleDelete],
    c_to_m_service: CToMServiceProtocol = Depends(ConceptService)
    ) -> None:
    """
    Removes a concept from a module
    """
    try:
        await c_to_m_service.delete_module_junctions(junctions=junctions)

    except DBError as e:
        response.status_code = e.status_code
        return ErrorResponse(
            code=e.status_code,
            type=e.type,
            message=str(e)
        )