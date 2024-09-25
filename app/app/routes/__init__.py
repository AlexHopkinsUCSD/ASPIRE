from fastapi import APIRouter
from fastapi.applications import FastAPI

from fastapi_lti1p3 import routes
from app.app.routes import (root, qas, domain, concept, concept_to_concept, concept_to_module,
                            module, course, question, gui, prompt, student, quiz)
from app.config.environment import get_settings
from app.domain.models.errors import APIMErrorResponse, ErrorResponse

def register_routers(app: FastAPI) -> FastAPI:
    settings = get_settings()
    app.router.prefix=settings.BASE_PATH
    app.router.responses |= {
        400: {"model": ErrorResponse}, 
        404: {"model": ErrorResponse}, 
        401: {"model": APIMErrorResponse}, 
        422: {"model": APIMErrorResponse}, 
        500: {"model": ErrorResponse}
        }

    app.include_router(root.router)
    app.include_router(routes.router)
    app.include_router(qas.router, tags=["QAS"], prefix="/qas")
    app.include_router(quiz.router, tags=["Quiz"], prefix="/aspire_quiz")
    app.include_router(domain.router, tags=["Domain"], prefix="/domain")
    app.include_router(concept.router, tags=["Concept"], prefix="/concept")
    app.include_router(concept_to_concept.router, tags=["ConceptToConcept"], prefix="/concept/cc")
    app.include_router(concept_to_module.router, tags=["ConceptToModule"], prefix="/concept/cm")
    app.include_router(module.router, tags=["Module"], prefix="/module")   
    app.include_router(course.router, tags=["Course"], prefix="/course")  
    app.include_router(question.router, tags=["Question"], prefix="/question")
    app.include_router(gui.router, tags=["GUI"], prefix="/gui")
    app.include_router(prompt.router, tags=["Prompt"], prefix="/prompt")
    app.include_router(student.router, tags=["Student"], prefix="/student")
    return app