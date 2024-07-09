from http.client import HTTPException
from typing import Optional, List

from fastapi import APIRouter, Depends, Form, HTTPException, Response, Request


router = APIRouter()


#Routes related to the Domain and Domain structure 
@router.put("/", name="domain:update-domain")
async def update_domain(
    request: Request,

    ):
    pass