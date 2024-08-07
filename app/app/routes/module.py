from typing import Optional, List, Union

from fastapi import APIRouter, Depends, Response, Request

from ..errors.db_error import DBError

from app.domain.models.errors import ErrorResponse

from app.domain.models.concept import ConceptRead

from app.domain.models.module import ModuleRead, ModuleUpdate, ModuleCreateNoLLM
from app.domain.services.module import ModuleService
from app.domain.protocols.services.module import ModuleService as ModuleServiceProtocol


router = APIRouter()

@router.post("/create/module", name="Module:create-module", response_model=Union[ModuleRead, ErrorResponse])
async def create_module(
    request: Request, 
    response: Response,
    module: ModuleCreateNoLLM,
    concepts: Optional[List[ConceptRead]] = None,
    module_service: ModuleServiceProtocol = Depends(ModuleService)
    ) -> Union[ModuleRead, ErrorResponse]:
    """
    Creates a new module and adds it to a domain and a course
    """
    #TODO: Update input structure to not require a domain_id
    try:
        return await module_service.create_module_no_llm(module=module, concepts=concepts)
    
    except DBError as e:
        response.status_code = e.status_code
        return ErrorResponse(
            code=e.status_code,
            type=e.type,
            message=str(e)
        )

@router.get("/get/{module_id}/module", name="Module:get-module", response_model=Union[ModuleRead, ErrorResponse])
async def get_module(
    request: Request, 
    response: Response,
    module_id: int,
    module_service: ModuleServiceProtocol = Depends(ModuleService)
    ) -> Union[ModuleRead, ErrorResponse]:
    """
    Returns a single module by its module_id
    """
    try:
        return await module_service.get_module(module_id=module_id)
    
    except DBError as e:
        response.status_code = e.status_code
        return ErrorResponse(
            code=e.status_code,
            type=e.type,
            message=str(e)
        )

@router.get("/get/{course_id}/course", name="Module:get-all-modules-of-course", response_model=Union[List[ModuleRead], ErrorResponse])
async def get_all_course_modules(
    request: Request, 
    response: Response,
    course_id: int,
    module_service: ModuleServiceProtocol = Depends(ModuleService)
    ) -> Union[List[ModuleRead], ErrorResponse]:
    """
    Returns all modules within a course
    """
    try:
        return await module_service.get_course_modules(course_id=course_id)

    except DBError as e:
        response.status_code = e.status_code
        return ErrorResponse(
            code=e.status_code,
            type=e.type,
            message=str(e)
        )

@router.get("/get/{domain_id}/domain", name="Module:get-all-modules-of-domain", response_model=Union[List[ModuleRead], ErrorResponse])
async def get_all_domain_modules(
    request: Request, 
    response: Response,
    domain_id: int,
    module_service: ModuleServiceProtocol = Depends(ModuleService)
    ) -> Union[List[ModuleRead], ErrorResponse]:
    """
    Returns all modules within a domain
    """
    try:
        return await module_service.get_domain_modules(domain_id=domain_id)
    
    except DBError as e:
        response.status_code = e.status_code
        return ErrorResponse(
            code=e.status_code,
            type=e.type,
            message=str(e)
        )

@router.get("/get/all", name="Module:get-all-modules", response_model=Union[List[ModuleRead], ErrorResponse])
async def get_all_modules(
    request: Request, 
    response: Response,
    module_service: ModuleServiceProtocol = Depends(ModuleService)
    ) -> Union[List[ModuleRead], ErrorResponse]:
    """
    Returns all modules
    """
    try:
        print("test")
        return await module_service.get_all_modules()
    
    except DBError as e:
        response.status_code = e.status_code
        return ErrorResponse(
            code=e.status_code,
            type=e.type,
            message=str(e)
        )

@router.put("/update/{module_id}", name="Module:get-all-modules", response_model=Union[ModuleRead, ErrorResponse])
async def update_module(
    request: Request, 
    response: Response,
    module_id: int,
    module_update: ModuleUpdate,
    module_service: ModuleServiceProtocol = Depends(ModuleService)
    ) -> Union[ModuleRead, ErrorResponse]:
    """
    Updates a module
    """
    try:
        return await module_service.update_module(module_id=module_id, module_update=module_update)
    
    except DBError as e:
        response.status_code = e.status_code
        return ErrorResponse(
            code=e.status_code,
            type=e.type,
            message=str(e)
        )

@router.delete("/delete/{module_id}/{course_id}", name="Module:delete-module-from-course")
async def delete_module_from_course(
    request: Request, 
    response: Response,
    module_id: int,
    course_id: int,
    module_service: ModuleServiceProtocol = Depends(ModuleService)
    ):
    """
    Removes a module from a course
    """
    try:
        return await module_service.delete_module_from_course(module_id=module_id, course_id=course_id)
    
    except DBError as e:
        response.status_code = e.status_code
        return ErrorResponse(
            code=e.status_code,
            type=e.type,
            message=str(e)
        )