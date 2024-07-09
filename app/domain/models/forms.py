from typing import Optional
from datetime import date
from fastapi import Form

from pydantic import BaseModel


class RegistrationForm(BaseModel):
    domain_id: Optional[int]
    instructor: str = Form(...),
    quarter: date = Form(...),
    name: Optional[str] = Form(None),
    subject: str = Form(...),
    difficulty: int = Form(...),
    
    @classmethod
    def as_form(
        cls,
        domain_id: Optional[int] = Form(None),
        instructor: str = Form(...),
        quarter: date = Form(...),
        name: Optional[str] = Form(None),
        subject: str = Form(...),
        difficulty: int = Form(...),
    ):
        name = name if name != None else f"{instructor} - {quarter}"
        print(f"name - str: {type(name)}\ninstructor-str: {type(instructor)}\nquarter-date: {type(quarter)}\nsubject-str: {type(subject)}\ndifficulty-int: {type(difficulty)}\nDomain_id: {domain_id}")
        return cls(domain_id=domain_id, instructor=instructor, quarter=quarter, name=name, subject=subject, difficulty=difficulty)
        # return RegistrationForm(domain_id=domain_id, instructor=instructor, quarter=quarter, name=name, subject=subject, difficulty=difficulty)
    

class ModuleForm(BaseModel):
    title: str = Form(...),
    course_id: int = Form(...)

    @classmethod
    def as_form(
        cls,
        title: str = Form(...),
        course_id: int = Form(...)
    ):
        return cls(title=title, course_id=course_id)