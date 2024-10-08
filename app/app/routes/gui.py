from fastapi import APIRouter, Depends, Form, HTTPException, Response, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/app/templates")

@router.get("")
async def get_spa(response: Response, request: Request):
    print(f"\n\n{request.body}\n\n")
    return templates.TemplateResponse("index.html", context={"request": request})