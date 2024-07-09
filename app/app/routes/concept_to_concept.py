from typing import List, Literal, Union

from fastapi import APIRouter, Depends, Response, Request

from app.domain.models.errors import ErrorResponse
from ..errors.db_error import DBError

from app.domain.models.concept import ConceptToConceptCreate, ConceptRead, ConceptToConceptDelete, ConceptBulkRead, ConceptToConceptRead
from app.domain.protocols.services.concept import ConceptToConceptService as CToCProtocol
from app.domain.services.concept import ConceptService


router = APIRouter()

@router.post("", name="ConceptToConcept:create-concept-to-concept-junction", response_model=Union[List[ConceptToConceptRead], ErrorResponse])
async def create_cc_junction(
    request: Request, 
    response: Response,
    junctions: List[ConceptToConceptCreate],
    c_to_c_service: CToCProtocol = Depends(ConceptService)
    ) -> Union[List[ConceptToConceptRead], ErrorResponse]:
    """
    Creates new ConceptToConcept junctions
    """
    try:
        return await c_to_c_service.bulk_create_concept_junctions(junctions=junctions)

    except DBError as e:
        response.status_code = e.status_code
        return ErrorResponse(
            code=e.status_code,
            type=e.type,
            message=str(e)
        )

@router.get("/{direction}/{concept_name}", name="ConceptToConcept:get-concept-to-concept-junctions", response_model=Union[List[ConceptToConceptRead], ErrorResponse])
async def get_concept_junctions(
    request: Request, 
    response: Response,
    direction: Literal["up", "down", "both"],
    concept_name: str,
    c_to_c_service: CToCProtocol = Depends(ConceptService)
    ) -> Union[List[ConceptToConceptRead], ErrorResponse]:
    """
    Returns all the concept-to-concept junctions of given concepts in the direction specified.
    | Input | Required | Type | Description |
    | :---- | :------- | :--- | :---------- |
    | direction | True | str["up", "down", "both"] | Direction refers to the orientation of the junction, "down" would return all the prerequisites of the supplied concept, "up" would return all the dependents of the supplied concept, and "both" returns both |
    | concept_name | True | str | The string name of a concept |

    """
    try:
        return await c_to_c_service.get_concept_junctions(concepts=ConceptBulkRead(concepts=[ConceptRead(name=concept_name)]), junction_direction=direction)

    except DBError as e:
        response.status_code = e.status_code
        return ErrorResponse(
            code=e.status_code,
            type=e.type,
            message=str(e)
        )

#TODO: add return for success or failure to delete
@router.delete("", name="ConceptToConcept:delete-concept-to-concept-junctions")
async def delete_concept_junction(
    request: Request, 
    response: Response,
    junctions: List[ConceptToConceptDelete],
    c_to_c_service: CToCProtocol = Depends(ConceptService)
    ) -> None:
    """
    Deletes one or many ConceptToConcept junctions
    """
    try:
        return await c_to_c_service.delete_junctions(junctions=junctions)

    except DBError as e:
        response.status_code = e.status_code
        return ErrorResponse(
            code=e.status_code,
            type=e.type,
            message=str(e)
        )