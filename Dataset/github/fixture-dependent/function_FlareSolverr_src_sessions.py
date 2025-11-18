from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Tuple
from uuid import uuid1
from selenium.webdriver.chrome.webdriver import WebDriver
import utils

@dataclass
class Session:
    session_id: str
    driver: WebDriver
    created_at: datetime

def create(self, session_id: Optional[str]=None, proxy: Optional[dict]=None, force_new: Optional[bool]=False) -> Tuple[Session, bool]:
    session_id = session_id or str(uuid1())
    if force_new:
        self.destroy(session_id)
    if self.exists(session_id):
        return (self.sessions[session_id], False)
    driver = utils.get_webdriver(proxy)
    created_at = datetime.now()
    session = Session(session_id, driver, created_at)
    self.sessions[session_id] = session
    return (session, True)