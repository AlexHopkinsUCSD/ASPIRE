import json
from pathlib import Path

from fastapi import APIRouter, Request, Response, Depends, Form
from fastapi.responses import RedirectResponse, JSONResponse

from fastapi_lti1p3 import enforce_auth, LTI
from fastapi_lti1p3.dynamic_registration import DynamicRegistrationService

from fastapi_lti1p3.utils import get_tool_public_key
from fastapi_lti1p3.errors.validation_errors import TokenValidationError
from fastapi_lti1p3.config import AdapterConfig
from fastapi.templating import Jinja2Templates
from fastapi_lti1p3.models import (
    RegistrationSchema, 
    CanvasToolConfiguration, 
    DefaultToolConfiguration, 
    CanvasMessageSchema, 
    DefaultMessageSchema
    )


from .errors import ClientIdError

router = APIRouter()

# BASE_PATH = Path(__file__).parent.resolve()

@router.get("/register/init")
async def dynamic_registration_init(
    request: Request,
    registration_service = Depends(DynamicRegistrationService)
    ):
    oidc_config = await registration_service.get_registration_config()
    _TOOL_SETTINGS = AdapterConfig().get_tool_settings().dict(by_alias=True)

    if oidc_config.get("issuer") == "https://canvas.instructure.com":
        default_tool_config = CanvasToolConfiguration(**_TOOL_SETTINGS)

    else:
        default_tool_config = DefaultToolConfiguration(**_TOOL_SETTINGS)

    default_settings = RegistrationSchema(**_TOOL_SETTINGS, lti_tool_configuration=default_tool_config)

    templates = Jinja2Templates(directory=_TOOL_SETTINGS.get("REGISTRATION_FRAME_REPO"))

    return templates.TemplateResponse(
        _TOOL_SETTINGS.get("DYNAMIC_REGISTRATION_TEMPLATE"), 
        context={
            "request": request, 
            "oidc_config": oidc_config,
            "default_config": default_settings.dict(by_alias=True)
            }) 



@router.get("/public_jwk")
async def get_public_jwk(request: Request):
    """
    Returns the public key for the platform to decode auth request tokens during oidc auth request
    """
    _TOOL_SETTINGS = AdapterConfig().get_tool_settings()
    return JSONResponse(
        content=await get_tool_public_key(_TOOL_SETTINGS)
    )


@router.post("/oidc/init")
async def oidc_init_post(request: Request):
    """
    POST endpoint for LTI 1.3 OIDC init stage
    """
    lti_adapter = LTI(request=request)
    try:
        auth_req_url = await lti_adapter.create_auth_response()


    except ClientIdError as e:
        return JSONResponse(content={"type": "ClientIdError", "details": e.message}, status_code=e.status_code)
    
    print(f"\n\n{auth_req_url}\n\n")

    return RedirectResponse(url=auth_req_url)


@router.get("/oidc/init")
async def oidc_init_get(request: Request):
    """
    GET endpoint for LTI 1.3 OIDC init stage
    """
    lti_adapter = LTI(request=request)
    auth_req_url = await lti_adapter.create_auth_response()
    return RedirectResponse(url=auth_req_url)


@router.post("/oidc/response")
async def oidc_auth_response(
    request: Request, 
    response: Response
    ):

    lti_adapter = LTI(request=request)
    # #TODO: Handle platform auth error response

    try: 
        session_id, _, target_link_uri, storage_target, validated_token = await lti_adapter.validateResponse()
        _SETTINGS = AdapterConfig()
        _TOOL_SETTINGS = _SETTINGS.get_tool_settings()
        _PLATFORM_SETTINGS = await _SETTINGS.get_platform_settings(client_id=validated_token["aud"])

        templates = Jinja2Templates(directory=_TOOL_SETTINGS.AUTH_FRAME_REPO)
        return templates.TemplateResponse(
            _TOOL_SETTINGS.AUTH_FRAME_TEMPLATE, 
            {
                "request": request, 
                "session_id": session_id, 
                "storage_target": storage_target, 
                "target_link_uri": target_link_uri,
                "oidc_auth_domain": _PLATFORM_SETTINGS.platform_auth_req_uri
            }
        )
    
    
    except TokenValidationError as e: 
        return JSONResponse(content={"Error": e.message}, status_code=e.status_code)

    
@router.get("/dev/init")
async def simulated_lti_init(    
    request: Request, 
    response: Response
):
    """
    ==============================
    --DISABLED OUTSIDE LOCAL DEV--
    ==============================

    Step 1 of the simulated LTI launch process: \n
    - Emulates the 3rd-party OIDC init login request redirect.
    """

    _TOOL_SETTINGS = AdapterConfig().get_tool_settings()
    if _TOOL_SETTINGS.ENV != "LOCAL":
        return JSONResponse(content="NotImplementedError", status_code=501)
    
    else:
        templates = Jinja2Templates(directory=_TOOL_SETTINGS.DEV_FRAME_REPO)   
        return templates.TemplateResponse("simulateOIDCInit.html", context={"request": request})


@router.post("/dev/auth")
async def simulated_oidc_auth(
    request: Request, 
    response: Response,
    lti_adapter = Depends(LTI)
):
    """
    ==============================
    --DISABLED OUTSIDE LOCAL DEV--
    ==============================

    Step 2 of the simulated LTI launch process: \n
    - Emulates the OIDC auth response redirect using the state generated in step 1 and the applications internal jwt endpoints.
    """
    _TOOL_SETTINGS = AdapterConfig().get_tool_settings()
    if _TOOL_SETTINGS.ENV != "LOCAL":
        return JSONResponse(content="NotImplementedError", status_code=501)
    
    else:
        data = dict(request.query_params)
        templates = Jinja2Templates(directory=_TOOL_SETTINGS.DEV_FRAME_REPO)  
        print(data.get("params"))
        token = await lti_adapter.create_jwt(aud=data["client_id"], nonce=data["nonce"], params=json.loads(data.get("params")))

        return templates.TemplateResponse("simulateOIDCAuth.html", context={"request": request, "id_token": token, "state": data["state"]})


@router.post("/dev/launch")
async def simulated_lti_launch(    
    request: Request, 
    session_id: str = Form(...),
    storage_target: str = Form(...),
    oidc_auth_domain: str = Form(...)
):
    """
    ==============================
    --DISABLED OUTSIDE LOCAL DEV--
    ==============================

    Step 3 of the simulated LTI launch process: \n
    - Performs the final serving of frontend content after a valid session has been created with the session_id stored as a cookie. 
    """
    _TOOL_SETTINGS = AdapterConfig().get_tool_settings()

    if _TOOL_SETTINGS.ENV != "LOCAL":
        return JSONResponse(content="NotImplementedError", status_code=501)
    
    else:
        templates = Jinja2Templates(directory=_TOOL_SETTINGS.DEV_FRAME_REPO)

        session_data = await enforce_auth(request=request, session_id=session_id)
        session_info = session_data.id_token.get("https://purl.imsglobal.org/spec/lti/claim/custom")

        if session_info:
            context_data = {**session_info, "storage_target": storage_target, "tool_domain": _TOOL_SETTINGS.default_domain}
        else:
            context_data = {"storage_target": storage_target, "tool_domain": _TOOL_SETTINGS.default_domain}

        response = templates.TemplateResponse("simulateLTILaunch.html", context={"request": request, "data": context_data})
        response.set_cookie(key="lti-session-id", value=session_id, samesite="strict", httponly=True)

        return response
