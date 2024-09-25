from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Request, Response, Depends, Form
from fastapi.templating import Jinja2Templates

from app.domain.models.errors import ErrorResponse
from app.config.environment import get_settings

from fastapi_lti1p3 import enforce_auth, LTI

router = APIRouter()

_SETTINGS = get_settings()

BASE_PATH = Path(__file__).parent.resolve()

templates = Jinja2Templates(directory="app/app/templates")

@router.post("/launch")
async def lti_launch(
    request: Request, 
    session_id: Optional[str] = Form(...),
    storage_target: str = Form(...),
    oidc_auth_domain: str = Form(...)
):
    session_data = await enforce_auth(request=request, session_id=session_id)
    
    session_info = session_data.id_token.get("https://purl.imsglobal.org/spec/lti/claim/custom")
    context_data = {**session_info, "storage_target": storage_target, "oidc_auth_domain": oidc_auth_domain, "tool_domain":_SETTINGS.default_domain}

    if storage_target == "cookie":
        response = templates.TemplateResponse(
            "index.html", 
            context={
                "request": request, 
                "data": context_data, 
                "session_params": {}
                }
            )
        
        response.set_cookie(key="lti-session-id", value=session_id, samesite="strict", httponly=True)
    
    else:
        response = templates.TemplateResponse(
            "index.html", 
            context={
                "request": request, 
                "data": context_data, 
                "session_params": {
                    "session_id": session_id,
                    }
                }
            )
    
    return response





