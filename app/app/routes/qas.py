# TODO: Discuss with team about the TZ for time operations.
import datetime
import json
from mimetypes import guess_type
from typing import Dict, List, Literal, Optional, Union

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    Request,
    Response,
    UploadFile,
)
from fastapi.responses import JSONResponse
from loguru import logger
from sqlmodel import Session

from app.domain.models.course import CourseRead
from app.domain.models.errors import ErrorResponse
from app.domain.models.forms import ModuleForm, RegistrationForm
from app.domain.models.llm_agent import ContingencyFunctions, Validator
from app.domain.models.module import ModuleConceptsResponse, ModuleRead, ModuleSummary
from app.domain.models.question import QuestionCreate
from app.domain.models.student import StudentCreate
from app.domain.models.trigger_event import TriggerEventCreate
from app.domain.protocols.routes.qas import (
    PersonalizedQuestionProtocol,
    PersonalizedQuizProtocol,
)
from app.domain.protocols.services.course import CourseService as CourseServiceProtocol
from app.domain.protocols.services.domain import DomainService as DomainServiceProtocol
from app.domain.protocols.services.module import ModuleService as ModuleServiceProtocol
from app.domain.protocols.services.personalization import KnowledgeStateParameters
from app.domain.services.canvas import CanvasCourseService
from app.domain.services.concept import ConceptService
from app.domain.services.course import CourseService
from app.domain.services.domain import DomainService
from app.domain.services.module import ModuleService
from app.domain.services.personalization import QuestionPersonalizationService
from app.domain.services.question import QuestionService
from app.domain.services.quiz import QuizService
from app.domain.services.student import StudentService
from app.domain.services.trigger_event import TriggerEventService
from app.infrastructure.database.db import get_db
from app.infrastructure.LLM.contingencies.general import check_valid_json
from app.infrastructure.LLM.contingencies.questions import (
    check_contents_question_list,
    check_has_key_questions,
    format_questions,
)
from app.infrastructure.LLM.llm_agent import LLMAgent
from app.utils.anonymization import hash_string_using_sha256
from app.utils.personalization import (
    convert_question_list_to_dataframe,
    extract_concept_names_from_concept_bulk_read,
    map_answers_to_questions,
)
from fastapi_lti1p3 import enforce_auth
from fastapi_lti1p3.session_cache import SessionCache

from ..errors.db_error import DBError
from ..errors.llm_response_error import LLMResponseError
from ..errors.validation_error import ValidationError

router = APIRouter()

@router.post("/register", name="qas:register", response_model=Union[CourseRead, ErrorResponse])
async def register(
    request: Request,
    response: Response,
    model_name: Literal["gpt-3.5-turbo", "gemini-1.5-pro-latest", "gpt-4o", "llama-3"],
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
    # Check if files are either text or PDF
    for content_file in content_files:
        mimetype, _ = guess_type(content_file.filename)
        if mimetype not in ['text/plain', 'application/pdf']:
            response.status_code = 400
            return ErrorResponse(code=400, detail="Invalid file type. Only text and PDF are allowed.")

    domain_is_new = False

    if not form_data.domain_id:
        domain_result = await domain_service.create_domain(domain=form_data)
        if isinstance(domain_result, ErrorResponse):
            response.status_code = domain_result.code
            return domain_result
        form_data.domain_id = domain_result.domain_id
        domain_is_new = True

    course_result = await course_service.create_course(form_data=form_data, content_files=content_files, domain_is_new=domain_is_new, model_name=model_name)
    if isinstance(course_result, ErrorResponse):
        response.status_code = course_result.code
        return course_result

    return course_result

@router.post("/module", name="qas:create-module", response_model=Union[ModuleRead, ErrorResponse])
async def create_module(
    request: Request,
    response: Response,
    model_name: Literal["gpt-3.5-turbo", "gemini-1.5-pro-latest", "gpt-4o", "llama-3"],
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


@router.post("/module/generate-summary", name="qas:generate-module-summary", response_model=ModuleSummary)
async def generate_module_summary(
    request: Request,
    response: Response,
    model_name: Literal["gpt-3.5-turbo", "gemini-1.5-pro-latest", "gpt-4o", "llama-3"],
    prompt: str,
    files: List[UploadFile] = File(...),
    form_data: ModuleForm = Depends(ModuleForm.as_form),
    module_service: ModuleServiceProtocol = Depends(ModuleService),
) -> ModuleSummary:
    try:
        module_data = await module_service.generate_module_summary(model_name=model_name, form_data=form_data, files=files, prompt=prompt)
        return module_data
    except (DBError, ValidationError, LLMResponseError) as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))
        

@router.post("/module/generate-concepts", name="qas:generate-module-concepts", response_model=ModuleConceptsResponse)
async def generate_module_concepts(
    request: Request,
    response: Response,
    model_name: Literal["gpt-3.5-turbo", "gemini-1.5-pro-latest", "gpt-4o", "llama-3"],
    prompt: str,
    files: List[UploadFile] = File(...),
    form_data: ModuleForm = Depends(ModuleForm.as_form),
    module_service: ModuleServiceProtocol = Depends(ModuleService)
) -> ModuleConceptsResponse:
    try:
        module_data = await module_service.generate_module_concepts(model_name=model_name, form_data=form_data, files=files, prompt=prompt)
        return module_data
    except (DBError, ValidationError, LLMResponseError) as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))

@router.post("/module/generate-prerequisites", name="qas:generate-module-prerequisites", response_model=Dict[str, List[Dict[str, List[str]]]])
async def generate_module_prerequisites(
    request: Request,
    response: Response,
    model_name: Literal["gpt-3.5-turbo", "gemini-1.5-pro-latest", "gpt-4o", "llama-3"],
    module_id: int,
    module_service: ModuleServiceProtocol = Depends(ModuleService)
) -> Dict[str, List[Dict[str, List[str]]]]:
    try:
        prerequisites = await module_service.generate_module_prerequisites(module_id=module_id, model_name=model_name)
        return prerequisites
    except (DBError, ValidationError, LLMResponseError) as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))

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
    model_name: Literal["gpt-3.5-turbo", "gemini-1.5-pro-latest", "gpt-4o", "llama-3"],
    module_id: int,
    quiz_type: Literal["prereq", "preview", "review"],
    prompt: str,
    num_questions: int,
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
    questions = await llm_agent.execute(action="questions", contingency_functions=contingency_functions, params= {
        "quiz_type": quiz_type,
        "model_name": model_name,
        "prompt": prompt,
        "num_questions": num_questions
    })
    return questions


@router.post(
        path="/quiz/personal/{module_id}/{quiz_type}",
        name="qas:generate_personalized_quiz_for_all_students",
        responses={
            404: {"model": ErrorResponse},
            400: {"model": ErrorResponse},
            500: {"model": ErrorResponse}
            }
        )
async def generate_personalized_quiz_for_all_students(
        quiz_params: PersonalizedQuizProtocol,
        question_service = Depends(QuestionService),
        concept_service = Depends(ConceptService)
) -> Dict:
    # ---------- extracts concepts to be tested -----------------
    # TODO: Build a switch case for different quiz types.
    if quiz_params.quiz_type != "prereq":
        return JSONResponse(
            status_code=404,
            content={
                "code": 404,
                "type": 'ValueError',
                "message": 'Only prereq is available currently'
                }
            )
    else:
        # TODO: Define an alternative strategy for extracting relevant concepts.
        concepts_json_results = await concept_service.get_all_prereqs_of_module(
            quiz_params.module_id
        )
    concepts_to_be_tested = await extract_concept_names_from_concept_bulk_read(
        concepts_object=concepts_json_results
    )

    # extracts potential questions
    questions = await question_service.get_all_questions_for_concepts(
        concept_list=concepts_to_be_tested
    )

    # ---------- Canvas Specific Code -----------------
    canvas_course_service = CanvasCourseService(
        access_token=quiz_params.canvas_access_token,
        course_id=quiz_params.canvas_course_id
    )
    student_ids = await canvas_course_service.get_student_ids_in_course()
    logger.info(f"{student_ids}")
    # ---------- End of Canvas Specific Code -----------------

    for student in student_ids:
        logger.info(f"Quiz creation for {student} in progress...")
        # TODO: Replace with student service DB Extraction.
        student_knowledge_state = {}

        personalization_service = QuestionPersonalizationService(
            knowledge_state=KnowledgeStateParameters(
                concept_list=concepts_to_be_tested,
                student_knowledge_state=student_knowledge_state,
                sme_concept_wise_importance=quiz_params.sme_input,
                sme_opinion_importance_factor=quiz_params.sme_importance
            ),
            questions=questions
        )

        personalized_questions = await personalization_service.get_personalized_questions(
            n_questions=quiz_params.n_questions
        )
        personalized_answers = await question_service.get_answers_for_questions(
            question_ids=[question.id for question in personalized_questions]
        )
        personalized_question_answers_object = await map_answers_to_questions(
            questions=personalized_questions,
            answers=personalized_answers
        )

        # ---------- Canvas Specific Code -----------------
        quiz = await canvas_course_service.create_personalized_practice_quiz(
            student_id=student,
            module_id=quiz_params.module_id,
            type_of_quiz=quiz_params.quiz_type
        )
        for question_answer_object in personalized_question_answers_object:
            await canvas_course_service.add_question_to_quiz(
                quiz=quiz,
                question=question_answer_object
            )
        # ---------- End of Canvas Specific Code -----------------
        logger.info(f"Quiz creation for {student} completed.")


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
    return result

# Ran into Swagger UI problems with GET request body. Will research it later!
@router.post(
        path="/quiz/personal/{module_id}/{quiz_type}/question",
        name="qas:get_one_question_for_student",
        responses={
            404: {"model": ErrorResponse},
            400: {"model": ErrorResponse},
            500: {"model": ErrorResponse}
            }
        )
async def get_personalized_question(
        request: Request,
        # question_params: PersonalizedQuestionProtocol,
        quiz_id: int,
        quiz_service = Depends(QuizService),
        question_service = Depends(QuestionService),
        concept_service = Depends(ConceptService),
        student_service = Depends(StudentService)
) -> Dict:
    # As of 27 Aug 2024, accepted roles is 'StudentEnrollment' only
    session_data = await enforce_auth(request=request, accepted_roles={'StudentEnrollment'})
    session_info = session_data.id_token.get('https://purl.imsglobal.org/spec/lti/claim/custom')
    session_cache = SessionCache()

    # Extract Quiz information
    question_params = await quiz_service.get_quiz_by_id(quiz_id=quiz_id)

    # ---------- extracts concepts to be tested -----------------
    concepts_to_be_tested = session_data.concepts_to_be_tested
    if not concepts_to_be_tested:
        if question_params.quiz_type == "prereq":
            concepts_json_results = await concept_service.get_all_prereqs_of_module(
                question_params.module_id
            )
        else:
            concepts_json_results = await concept_service.get_all_concepts_in_module(
                question_params.module_id
            )
        concepts_to_be_tested = await extract_concept_names_from_concept_bulk_read(
            concepts_object=concepts_json_results
        )
        logger.debug(concepts_to_be_tested)
        session_data = await session_cache.set(
            cache_id=session_data.session_id,
            key='concepts_to_be_tested',
            value=concepts_to_be_tested,
            store="session"
        )
        logger.debug('Concept List added to Session Cache.')

    if not concepts_to_be_tested:
        return ErrorResponse(
            code=404,
            type="NoConceptsFoundError",
            message="There are no concepts provided to query the questions. Please check."
        )

    # Questions related to the Concepts
    if session_data.question_ids:
        questions = await question_service.get_questions_by_id(id_list=session_data.question_ids)
    else:
        logger.debug(concepts_to_be_tested)
        questions = await question_service.get_all_questions_for_concepts(
            concept_list=concepts_to_be_tested
        )
        question_ids = [question.id for question in questions]
        session_data = await session_cache.set(
            cache_id=session_data.session_id,
            key='question_ids',
            value=question_ids,
            store="session"
        )
        logger.debug(question_ids)
        logger.debug('Question List added to Session Cache.')

    if not questions:
        return ErrorResponse(
            code=404,
            type="NoQuestionsFoundError",
            message="There are no questions remaining/existing for given concept list."
        )

    # Get student knowledge
    # TODO: Ask the team if we can store this in session data.
    if not session_data.knowledge_state:
        student_knowledge_state = {}
        for concept in concepts_to_be_tested:
            c_to_k = await student_service.get_student_knowledge_score(
                student_id=session_info.get('user_id'),
                concept_name=concept
            )
            student_knowledge_state[concept] = 0.5 if not c_to_k else c_to_k

        session_data = await session_cache.set(
            cache_id=session_data.session_id,
            key='knowledge_state',
            value=student_knowledge_state,
            store="session"
        )
        logger.debug('Student Knowledge State added to Session Cache.')

    # Get Personalized Information
    personalization_service = QuestionPersonalizationService(
        knowledge_state=KnowledgeStateParameters(
            concept_list=concepts_to_be_tested,
            student_knowledge_state=session_data.knowledge_state,
            sme_concept_wise_importance=question_params.sme_input,
            sme_opinion_importance_factor=question_params.sme_importance
        ),
        questions=questions
    )
    question = await personalization_service.get_one_question()
    answers = await question_service.get_answers_for_one_question(
        question_id=question.id
    )

    # Remove the question from the list
    question_ids = [id for id in session_data.question_ids if id != question.id]
    await session_cache.set(
        cache_id=session_data.session_id,
        key='question_ids',
        value=question_ids,
        store="session"
    )
    logger.debug(f'Session Cache updated by removing question no. {question.id}.')

    return {'question': question, 'answers': list(answers)}


@router.post(
        path="/quiz/{module_id}/{quiz_type}/concepts",
        name="qas:get_concept_list",
        responses={
            404: {"model": ErrorResponse},
            400: {"model": ErrorResponse},
            500: {"model": ErrorResponse}
            }
        )
async def get_concept_list(
        module_id: int,
        quiz_type: Literal['prereq', 'preview', 'review'],
        concept_service = Depends(ConceptService)
) -> List:
    # TODO: Build a switch case for different quiz types.
    if quiz_type != "prereq":
        return JSONResponse(
            status_code=404,
            content={
                "code": 404,
                "type": 'ValueError',
                "message": 'Only prereq is available currently'
            }
        )

    concepts_json_results = await concept_service.get_all_prereqs_of_module(
        module_id
    )
    return await extract_concept_names_from_concept_bulk_read(
        concepts_object=concepts_json_results
    )


@router.put(
        path="/quiz/clear_cache",
        name="qas:clear_session_cache",
        responses={
            404: {"model": ErrorResponse},
            400: {"model": ErrorResponse},
            500: {"model": ErrorResponse}
            }
        )
async def clear_session_cache(request: Request) -> None:
    session_data = await enforce_auth(request=request, accepted_roles={'StudentEnrollment'})
    session_cache = SessionCache()

    await session_cache.set(
        cache_id=session_data.session_id,
        key='question_ids',
        value=[],
        store="session"
    )

    await session_cache.set(
        cache_id=session_data.session_id,
        key='concepts_to_be_tested',
        value=[],
        store="session"
    )



@router.put(
        path="/quiz/question/submit",
        name="qas:submit_an_answer",
        responses={
            404: {"model": ErrorResponse},
            400: {"model": ErrorResponse},
            500: {"model": ErrorResponse}
            }
        )
async def on_submit(
        request: Request,
        concept_name: str,
        value_of_question: Union[float, int],
        confidence_rating_of_question: float,
        student_service = Depends(StudentService),
        trigger_event_service = Depends(TriggerEventService)
) -> None:
    session_data = await enforce_auth(request=request, accepted_roles={'StudentEnrollment'})
    session_info = session_data.id_token.get('https://purl.imsglobal.org/spec/lti/claim/custom')

    # Prepare the student object
    student = await student_service.get_student(
        canvas_id=hash_string_using_sha256(session_info.get("user_id"))
    )
    if not student:
        logger.debug("Student not found. Creation in progress...")
        student = await student_service.add_student(
            student=StudentCreate(canvas_id=hash_string_using_sha256(session_info.get("user_id")))
        )
        logger.debug(student.id)
        await student_service.add_student_to_course(
            student_id=student.id,
            course_id=session_info.get('course_id')
        )

    # Create a trigger event entry in the DB.
    await trigger_event_service.add_event(
        event = TriggerEventCreate(
            datetime_stamp=datetime.datetime.now(),
            student_id=student.id,
            concept=concept_name,
            value=value_of_question,
            weight=confidence_rating_of_question
        )
    )