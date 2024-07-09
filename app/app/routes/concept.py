from typing import List, Union

from fastapi import APIRouter, Depends, Response, Request

from ..errors.db_error import DBError
from app.domain.models.errors import ErrorResponse

from app.domain.models.concept import ConceptCreate, ConceptCreateBulkRead, ConceptRead, ConceptFilter, ConceptReadVerbose
from app.domain.protocols.services.concept import ConceptService as ConceptServiceProtocol
from app.domain.services.concept import ConceptService

router = APIRouter()

# @router.post("/add", name="concept:add-concept", response_model=Union[ConceptRead, ErrorResponse])
# async def add_concept(
#     request: Request,
#     response: Response,
#     concept: ConceptCreate,
#     concept_service: ConceptServiceProtocol = Depends(ConceptService)
#     ) -> Union[ConceptRead, ErrorResponse]:
#     """
#     Adds a single concept to the DB
#     """
#     try:
#         return await concept_service.create_concept(concept=concept)
    
#     except DBError as e:
#         response.status_code = e.status_code
#         return ErrorResponse(
#             code=e.status_code,
#             type=e.type,
#             message=str(e)
#         )


@router.post("", name="Concept:add-concepts", response_model=Union[ConceptCreateBulkRead, ErrorResponse])
async def add_concepts(
    request: Request,
    response: Response,
    concepts: List[ConceptCreate],
    concept_service: ConceptServiceProtocol = Depends(ConceptService)
    ) -> Union[ConceptCreateBulkRead,ErrorResponse]:
    """
    Adds one or many concepts to the DB and assigns them to a course and domain
    """
    try:
        return await concept_service.bulk_create_concepts(concepts=concepts)
    
    except DBError as e:
        response.status_code = e.status_code
        return ErrorResponse(
            code=e.status_code,
            type=e.type,
            message=str(e)
        )


@router.get("/{concept_name}", name="Concept:get-concepts", response_model=Union[ConceptReadVerbose, ErrorResponse])
async def get_concept(
    request: Request, 
    response: Response,
    concept_name: str,
    concept_service: ConceptServiceProtocol = Depends(ConceptService)
    ) -> Union[ConceptReadVerbose, ErrorResponse]:
    """
    Returns the details of a specific concept
    """
    try:
        return await concept_service.get_concept(concept_name=concept_name, read_mode="verbose")
    
    except DBError as e:
        response.status_code = e.status_code
        return ErrorResponse(
            code=e.status_code,
            type=e.type,
            message=str(e)
        )


@router.get("/filter/{filter}", name="Concept:get-concepts-by-filter", response_model=Union[List[ConceptReadVerbose], ErrorResponse])
async def get_concept_filtered(
    request: Request, 
    response: Response,
    filter: ConceptFilter = Depends(ConceptFilter),
    concept_service: ConceptServiceProtocol = Depends(ConceptService)
    ) -> Union[List[ConceptReadVerbose], ErrorResponse]:
    """
    Returns all concepts matching the supplied filters
    """
    try:
        return await concept_service.get_many_concepts(filters=filter, read_mode="verbose")
    
    except DBError as e:
        response.status_code = e.status_code
        return ErrorResponse(
            code=e.status_code,
            type=e.type,
            message=str(e)
        )

