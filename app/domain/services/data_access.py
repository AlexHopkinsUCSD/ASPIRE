from typing import List, Optional, Set, Literal
from fastapi import Request, Depends

from fastapi_lti1p3 import Session, enforce_auth

from app.domain.protocols.services.data_access import DataAccessService as DataAccessServiceProtocol
from app.domain.models.data_access import DataAccess, AccessCertificate

from app.domain.services.module import ModuleService
from app.domain.protocols.services.module import ModuleService as ModuleServiceProtocol

class DataAccessService(DataAccessServiceProtocol):
    def __init__(self, request) -> None:
        self.request: Request = request
        self.module_service: ModuleServiceProtocol = Depends(ModuleService)

    async def _accessible_modules(self, session_data: Session) -> List[AccessCertificate]:
        session_params = session_data.id_token.get("https://purl.imsglobal.org/spec/lti/claim/custom")
        course_id = session_params.get("course_id")
        client_roles = session_data.get_roles()

        course_modules = await self.module_service.get_course_modules(course_id=course_id, id_only=True)
        access_certificates = []

        if set(client_roles).issubset({"DesignerEnrollment", "TeacherEnrollment"}):
            access_certificates.append(AccessCertificate(entry_ids="all", access_rights=["read"]))
            access_certificates.append(AccessCertificate(entry_ids=set(course_modules), access_rights={"read", "write", "delete"}))
        
        else:
            access_certificates.append(AccessCertificate(entry_ids=set(course_modules), access_rights={"read"}))
        
        return access_certificates


    #TODO: Add additional AccessCertificate generation
    async def _accessible_courses(self, session_data: Session, accepted_roles: Optional[Set[str]]) -> List[AccessCertificate]:
        pass

    async def _accessible_student_data(self, session_data: Session, accepted_roles: Optional[Set[str]]) -> List[AccessCertificate]:
        pass

    async def __call__(
        self, 
        accepted_roles: Optional[Set[str]], 
        data_targets: List[Literal["module_access", "course_access", "student_access"]],
    ) -> DataAccess:
        session_data: Session = await enforce_auth(request=self.request, accepted_roles=accepted_roles)

        callables = {
            "module_access": self._accessible_modules, 
            "course_access": self._accessible_courses, 
            "student_access": self._accessible_student_data
        }
        data_access = {}

        for target in data_targets:
            data_access[target] = await callables[target](session_data=session_data)

        return DataAccess(**data_access, session=session_data)

    