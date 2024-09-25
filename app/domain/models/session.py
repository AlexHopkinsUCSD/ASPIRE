from fastapi_lti1p3 import Session
from typing import Optional, List, Dict

class SessionExtended(Session):
    params: Optional[dict] = {}
    concepts_to_be_tested: Optional[List] = []
    question_ids: Optional[List] = []
    knowledge_state: Optional[Dict] = {}
