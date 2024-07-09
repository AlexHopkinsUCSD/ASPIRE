from pathlib import Path

from fastapi import APIRouter, Request, Response, Depends
from fastapi.responses import RedirectResponse, JSONResponse

from fastapi_lti1p3.lti1p3 import LTI
from fastapi_lti1p3.errors.validation_errors import TokenValidationError
from fastapi.templating import Jinja2Templates

router = APIRouter()

BASE_PATH = Path(__file__).parent.resolve()

templates = Jinja2Templates(directory="app/app/templates")

# @router.get("/oidc/config")
# async def get_config_json(request: Request, response: Response):
#     lti_adapter = LTI(request=request, response=response)
#     registration_endpoint = request.query_params.get("openid_configuration")
#     registration_token = request.query_params.get("registration_token")
#     openid_config_response = requests.get(url=registration_endpoint, headers={"Authorization": f"Bearer {registration_token}"})
#     # openid_config.text
#     openid_config = json.loads(openid_config_response.content)
#     return JSONResponse(content= await lti_adapter.get_developer_key_json(tool_public_jwk_url=f"{_SETTINGS.DOMAIN_NAME}/oidc/public_jwk"))


# @router.get("/oidc/public_jwk")
# async def get_public_jwk(request: Request, lti_adapter=Depends(LTI)):
#     """
#     Returns the public key for the platform to decode auth request tokens during oidc auth request
#     """
#     return JSONResponse(
#         content=await lti_adapter.get_tool_public_key()
#     )


# @router.post("/oidc/init")
# async def oidc_init_post(request: Request):
#     """
#     POST endpoint for LTI 1.3 OIDC init stage
#     """
#     #TODO: identify actual way canvas sends these arguments, might need to dig through the headers for them
#     lti_adapter = LTI(request=request)
#     auth_req_url = await lti_adapter.create_auth_response()
#     return RedirectResponse(url=auth_req_url)


# @router.get("/oidc/init")
# async def oidc_init_get(request: Request):
#     """
#     GET endpoint for LTI 1.3 OIDC init stage
#     """
#     lti_adapter = LTI(request=request)
#     auth_req_url = lti_adapter.create_auth_response()
#     return RedirectResponse(url=auth_req_url)


# @router.post("/oidc/response")
# async def oidc_auth_response(
#     request: Request, 
#     response: Response
#     ):
#     lti_adapter = LTI(request=request)
#     #TODO: Handle platform auth error response
#     try: 
#         session_id, csrf_token, target_link_uri = await lti_adapter.validateResponse()
#         response = RedirectResponse(url=target_link_uri, status_code=303)
#         response.set_cookie(key="session_id", value=session_id, httponly=True, secure=True, samesite="strict")
#         return response

#     except TokenValidationError as e: 
#         return JSONResponse(content={"Error": e.message}, status_code=e.status_code)


@router.get("/oidc/launch")
async def lti_launch(
    request: Request, 
    response: Response
):
    return templates.TemplateResponse("index.html", context={"request": request})
