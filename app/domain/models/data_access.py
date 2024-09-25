from typing import List, Literal, Optional, Set, Union, Tuple
from pydantic import BaseModel

from fastapi_lti1p3 import Session

class AccessBase(BaseModel):
    entry_ids: Union[Set[int], Literal["all"]]
    access_rights: Set[Literal["read", "write", "delete"]]

class AccessCertificate(AccessBase):
    pass

class CompliancePolicy(AccessBase):
    pass


class DataAccessError(Exception):
    def __init__(
            self, 
            data_target: Literal["module_access", "course_access", "student_access"], 
            compliance_policy: CompliancePolicy, 
        ) -> None:

        self.data_target = data_target
        self.compliance_policy = compliance_policy

    def __str__(self):
        return f"""
        Unauthorized Access - Target resource(s) {self.compliance_policy.entry_ids} requires {self.data_target} and {self.compliance_policy.access_rights} rights.
        """


class DataAccess(BaseModel):
    session: Session
    module_access: Optional[List[AccessCertificate]]
    course_access: Optional[List[AccessCertificate]]
    student_access: Optional[List[AccessCertificate]]
    
    async def _failure(
        self, 
        compliance_policy: CompliancePolicy,
        data_target: Literal["module_access", "course_access", "student_access"],
        failure_mode: Literal["safe", "deadly"] = "safe",
    ):
        if failure_mode == "deadly":
            raise DataAccessError(
                data_target=data_target, 
                compliance_policy=compliance_policy,
            )
        
        else:
            target_options = self.dict()
            access_data = target_options.get(data_target)

            for cert in access_data:
                if compliance_policy.access_rights == cert.access_rights:
                    try:
                        entry_intersection = cert.entry_ids.intersection(compliance_policy.entry_ids)
                        return False, CompliancePolicy(entry_ids=entry_intersection, access_rights=compliance_policy.access_rights)
                    except Exception as e:
                        # If the offending cert with the requested access rights fails due to an 'all' policy slipping through, then the policy should have passed and returned
                        if cert.entry_ids == "all":
                            return True, 
            return False, CompliancePolicy(entry_ids={}, access_rights={})

    async def has_access(
        self, 
        data_target: Literal["module_access", "course_access", "student_access"],
        compliance_policy: CompliancePolicy,
        failure_mode: Literal["safe", "deadly"] = "safe"
    ) -> Tuple[bool, CompliancePolicy]:
        """
        Compares the entry_ids and access_rights of the CompliancePolicy supplied by the data service receiving a DataAccess object with the targeted AccessCertificate group of the client.
        If the CompliancePolicy is a subset of any AccessCertificate, the function returns both True and with the original CompliancePolicy. 
        This means the entry_ids of the CompliancePolicy are all acceptable to be returned to the client.

        If no match is found, the function has two failure modes dependent on what has been specified:

        - failure_mode='safe' searches for an AccessCertificate matching the required 'access_rights' specified on the CompliancePolicy, 
        creates a new CompliancePolicy where the entry_ids are the intersection of the CompliancePolicy and AccessCertificate, 
        thus removing any requested ids not allowed by the AccessCertificate. Data should only be returned if the id exists in a returned CompliancePolicy.

        -failure_mode='deadly' immediately raises a DataAccessError which should be caught and result in the return of an ErrorResponse to the client.
        """

        target_options = self.dict()
        access_data = target_options.get(data_target)

        if access_data is None:
            return self._failure(
                failure_mode=failure_mode, 
                compliance_policy=compliance_policy, 
                data_target=data_target
                )

        access_granted = False
        for cert in access_data:
            # All values of the compliance policies access rights must be contained by the AccessCertificate,
            # and the entry_ids of the policy either all have to exist on the cert or the cert must specify "all" ids are valid
            if compliance_policy.access_rights.issubset(cert.access_rights) and (compliance_policy.entry_ids.issubset(cert.entry_ids) or cert.entry_ids == "all"):
                access_granted = True

        if not access_granted:
            return self._failure(
                failure_mode=failure_mode, 
                compliance_policy=compliance_policy, 
                data_target=data_target
                )
        
        return access_granted, compliance_policy