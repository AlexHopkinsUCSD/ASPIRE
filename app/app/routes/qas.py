from mimetypes import guess_type
from sqlmodel import Session
from typing import Optional, List, Literal, Union
from fastapi import APIRouter, Depends, File, Response, Request, UploadFile
from fastapi.responses import JSONResponse

from app.infrastructure.database.db import get_db

from app.domain.models.errors import ErrorResponse
from ..errors.db_error import DBError
from ..errors.validation_error import ValidationError
from ..errors.llm_response_error import LLMResponseError

from app.domain.protocols.services.course import CourseService as CourseServiceProtocol
from app.domain.services.course import CourseService
from app.domain.models.course import CourseRead
from app.domain.models.forms import RegistrationForm, ModuleForm

from app.domain.protocols.services.domain import DomainService as DomainServiceProtocol
from app.domain.services.domain import DomainService

from app.domain.protocols.services.module import ModuleService as ModuleServiceProtocol
from app.domain.services.module import ModuleService
from app.domain.models.module import ModuleRead

from app.infrastructure.LLM.llm_agent import LLMAgent
from app.domain.models.llm_agent import Validator, ContingencyFunctions

from app.domain.models.question import QuestionCreate

from app.infrastructure.LLM.contingencies.questions import format_questions, check_contents_question_list, check_has_key_questions
from app.infrastructure.LLM.contingencies.general import check_valid_json


router = APIRouter()

# Routes related to the Quiz Authoring System
@router.post("/register", name="qas:reigster", response_model=Union[CourseRead, ErrorResponse])
async def register(
    request: Request,
    response: Response,
    model_name: Literal["gpt-3.5-turbo", "gemini-1.5-pro-latest"],
    content_files: List[UploadFile] = File(...),
    form_data: RegistrationForm = Depends(RegistrationForm.as_form),
    course_service: CourseServiceProtocol = Depends(CourseService),
    domain_service: DomainServiceProtocol = Depends(DomainService),
    ) -> Union[CourseRead, ErrorResponse]:
    """
    Registers a new course in the system, assigns a domain and LLM-generated content summary to the course.\n

    | Input | Required | Type | Description |
    | :---- | :------: | :--: | :---------- |
    | files | True | List of Files | Course contents either as an image or text file, used to generate content summary and domain concepts when a new domain is created |
    | domain_id | False | Int | Reuses an existing domain if supplied, generates a new domain from the content files if not supplied |
    | instructor | True | Str | Name of instructor |
    | quarter | True | Date | Quarter start date |
    | name | False | Str | Name of course, uses 'instructor - quarter' if no name is supplied |
    | subject | True | Str | Subject of course |
    | difficulty | True | Int | Difficulty level of course coded as Int (1: introductory, 2: intermediate, 3: undergrad?, ...) final code tbd |
    """
    #TODO: Finalize difficulty scale/code
    # Check if files are either text or PDF
    print(form_data)
    for content_file in content_files:
        mimetype, _ = guess_type(content_file.filename)
        if mimetype not in ['text/plain', 'application/pdf']:
            response.status_code = 400
            return ErrorResponse(code=400, detail="Invalid file type. Only text and PDF are allowed.")

    domain_is_new = False

    if not form_data.domain_id:
        result = await domain_service.create_domain(domain=form_data)
        form_data.domain_id  = result.domain_id
        domain_is_new = True

    if isinstance(result, ErrorResponse):
        response.status_code = result.code

    result = await course_service.create_course(form_data=form_data, content_files=content_files, domain_is_new=domain_is_new, model_name=model_name)

    return result


@router.post("/module", name="qas:create-module", response_model=Union[ModuleRead, ErrorResponse])
async def create_module(
    request: Request,
    response: Response,
    model_name: Literal["gpt-3.5-turbo", "gemini-1.5-pro-latest"],
    files: List[UploadFile] = File(...),
    form_data: ModuleForm = Depends(ModuleForm.as_form),
    module_service: ModuleServiceProtocol = Depends(ModuleService)
    ) -> Union[ModuleRead, ErrorResponse]:
    """
    | Input | Required | Type | Description |
    | :---- | :------: | :--: | :---------- |
    | files | True | List of Files | Module contents either as an image or text file, used to generate content summary, module concepts, and prerequisite relationships |
    | title | True | Str | Title of Module |
    | course_id | True | ID of course module is being created for |  
    """
    try:
        result = await module_service.create_module(form_data=form_data, files=files, model_name=model_name)
        return result
    
    except (DBError, ValidationError, LLMResponseError) as e:
        return JSONResponse(
            status_code=e.status_code, 
            content={
                "code": e.status_code, 
                "type": e.__class__.__name__ if e.__class__.__name__ != "DBError" else e.type,
                "message": str(e)
                }
            )


@router.get(
        path="/quiz/{module_id}/{quiz_type}", 
        name="qas:get-quiz-questions",
        responses={
            404: {"model": ErrorResponse}, 
            400: {"model": ErrorResponse}, 
            500: {"model": ErrorResponse}
            }
        )
async def get_quiz_questions(
    request: Request,
    model_name: Literal["gpt-3.5-turbo", "gemini-1.5-pro-latest"],
    module_id: int,
    quiz_type: Literal["prereq", "preview", "review"],
    db: Session = Depends(get_db)
    ) -> List[QuestionCreate]:

    llm_agent = LLMAgent(module_id=module_id)
    
    contingency_functions = ContingencyFunctions(
        validators=[
                Validator(order=1, function=check_valid_json),
                Validator(order=2, function=check_has_key_questions),
                Validator(order=3, function=check_contents_question_list)
            ], 
        formatter=format_questions
        )
    #TODO: adjust formatter output
    questions = await llm_agent.execute(action="questions", contingency_functions=contingency_functions, params= {"quiz_type": quiz_type, "model_name": model_name})
    # print(result)
    return questions


@router.post("/quiz", name="qas:create-quiz")
async def create_quiz(
    request: Request,
    action: str,
    course_id: Optional[int]=None,
    module_id: Optional[int]=None,
    quiz_type: Optional[str]=None,
    content_files: Optional[List[UploadFile]] = File(None),
    ):
    #TODO: Add questions to question bank, return a QTI .ZIP file
    async def test_valid(response, *args, **kwargs):
        return "PASS", response
    
    async def test_format(response, validator_status, params):
        return response
    
    test = LLMAgent(content_files=content_files, course_id=course_id, module_id=module_id)
    contingency_functions = ContingencyFunctions(validators=[Validator(order=1, function=test_valid)], formatter=test_format)
    result = await test.execute(action=action, contingency_functions=contingency_functions, params={} if not quiz_type else {"quiz_type": quiz_type})
    print(type(result))

