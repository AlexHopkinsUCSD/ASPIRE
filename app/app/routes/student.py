from typing import Optional, List, Union

from fastapi import APIRouter, Depends, Response, Request

from ..errors.db_error import DBError

from app.domain.models.errors import ErrorResponse


from app.domain.protocols.services.trigger_event import TriggerEventService as TriggerEventServiceProtocol
from app.domain.services.trigger_event import TriggerEventService
from app.domain.models.trigger_event import TriggerEventCreate, TriggerEventRead

from app.domain.protocols.services.student import StudentService as StudentServiceProtocol
from app.domain.services.student import StudentService
from app.domain.models.student import StudentRead, StudentCreate, StudentToCourseCreate


router = APIRouter()


@router.post("", name="Student:add-student", response_model=Union[StudentRead, ErrorResponse])
async def add_student(    
    request: Request, 
    response: Response,
    student: StudentCreate,
    student_service: StudentServiceProtocol = Depends(StudentService)
    ):
    """
    Adds a new student to the db using their canvas_id
    """
    try:
        return await student_service.add_student(student=student)
    
    except DBError as e:
        response.status_code = e.status_code
        return ErrorResponse(
            code=e.status_code,
            type=e.type,
            message=str(e)
        )

@router.post("/course", name="Student:add-student-to-course", response_model=Union[StudentToCourseCreate, ErrorResponse])
async def add_student_to_course(    
    request: Request, 
    response: Response,
    student_id: int,
    course_id: int,
    student_service: StudentServiceProtocol = Depends(StudentService)
    ) -> Union[StudentToCourseCreate, ErrorResponse]:
    """
    Registers a student to a course registered in our system
    """
    try:
        return await student_service.add_student_to_course(student_id=student_id, course_id=course_id)
    
    except DBError as e:
        response.status_code = e.status_code
        return ErrorResponse(
            code=e.status_code,
            type=e.type,
            message=str(e)
        )
    

@router.post("/event", name="Student:add-event", response_model=Union[TriggerEventRead, ErrorResponse])
async def add_event(
    request: Request, 
    response: Response,
    event: TriggerEventCreate,
    event_service: TriggerEventServiceProtocol = Depends(TriggerEventService)
    ) -> Union[TriggerEventRead, ErrorResponse]:
    """
    Adds a new trigger event to the queue, Trigger Events 
    """
    try:
        return await event_service.add_event(event=event)
    
    except DBError as e:
        response.status_code = e.status_code
        return ErrorResponse(
            code=e.status_code,
            type=e.type,
            message=str(e)
        )


@router.post("/event/bulk", name="Student:add-many-events", response_model=Union[List[TriggerEventRead], ErrorResponse])
async def add_many_events(
    request: Request, 
    response: Response,
    events: List[TriggerEventCreate],
    event_service: TriggerEventServiceProtocol = Depends(TriggerEventService)
    ) -> Union[List[TriggerEventRead], ErrorResponse]:
    try:
        return await event_service.bulk_add_events(events=events)

    except DBError as e:
        response.status_code = e.status_code
        return ErrorResponse(
            code=e.status_code,
            type=e.type,
            message=str(e)
        )