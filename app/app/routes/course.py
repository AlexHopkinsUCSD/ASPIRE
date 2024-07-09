from typing import Optional, List, Union
from fastapi import APIRouter, Depends, Form, HTTPException, Response, Request

from ..errors.db_error import DBError
from app.domain.models.errors import ErrorResponse

from app.domain.models.course import CourseCreateAPI, CourseFilter, CourseUpdate, CourseRead, CourseReadVerbose
from app.domain.protocols.services.course import CourseService as CourseServiceProtocol
from app.domain.services.course import CourseService


router = APIRouter()

@router.post("", name="Course:create-course", response_model=Union[CourseRead, ErrorResponse])
async def create_course(
    request: Request, 
    response: Response,
    course: CourseCreateAPI,
    course_service: CourseServiceProtocol = Depends(CourseService)
    ) -> Union[CourseRead, ErrorResponse]:
    """
    Creates a new course
    """
    try:
        return await course_service.create_course_no_llm(course=course)
    
    except DBError as e:
        response.status_code = e.status_code
        return ErrorResponse(
            code=e.status_code,
            type=e.type,
            message=str(e)
        )


@router.get("/{course_id}", name="Course:get-course", response_model=Union[CourseReadVerbose, ErrorResponse])
async def get_course(
    request: Request, 
    response: Response,
    course_id: int,
    course_service: CourseServiceProtocol = Depends(CourseService)
    ) -> Union[CourseReadVerbose, ErrorResponse]:
    """
    Returns a single course
    """
    try:
        return await course_service.get_one_course(course_id=course_id, read_mode="verbose")
    
    except DBError as e:
        response.status_code = e.status_code
        return ErrorResponse(
            code=e.status_code,
            type=e.type,
            message=str(e)
        )

@router.get("/filter/{course_filter}", name="Course:get-all-courses-matching-filter", response_model=Union[list[CourseReadVerbose], ErrorResponse])
async def get_matching_courses(
    request: Request, 
    response: Response,
    course_filter: CourseFilter = Depends(CourseFilter),
    course_service: CourseServiceProtocol = Depends(CourseService)
    ) -> Union[list[CourseReadVerbose], ErrorResponse]:
    """
    Returns all courses matching the provided filters
    """
    try:
        return await course_service.get_matching_courses(filters=course_filter)
    
    except DBError as e:
        response.status_code = e.status_code
        return ErrorResponse(
            code=e.status_code,
            type=e.type,
            message=str(e)
        )

@router.put("/{course_id}", name="Course:update-course", response_model=Union[CourseReadVerbose, ErrorResponse])
async def update_course(
    request: Request, 
    response: Response,
    course_id: int,
    course_update: CourseUpdate,
    course_service: CourseServiceProtocol = Depends(CourseService)
    ) -> Union[CourseReadVerbose, ErrorResponse]:
    """
    Updates a Course
    """
    try:
        return await course_service.update_course(course_id=course_id, course_update=course_update)
    
    except DBError as e:
        response.status_code = e.status_code
        return ErrorResponse(
            code=e.status_code,
            type=e.type,
            message=str(e)
        )
#TODO: Add return for success or failure to delete
@router.delete("/{course_id}", name="Course:delete-course")
async def delete_course(
    request: Request, 
    response: Response,
    course_id: int,
    course_service: CourseServiceProtocol = Depends(CourseService)
    ):
    """
    Deletes a course and all corresponding relationships
    """
    try:
        return await course_service.delete_course(course_id=course_id)
    
    except DBError as e:
        response.status_code = e.status_code
        return ErrorResponse(
            code=e.status_code,
            type=e.type,
            message=str(e)
        )