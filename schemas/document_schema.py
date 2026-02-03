from pydantic import BaseModel
from typing import Optional
import datetime


class Document(BaseModel):
    uuid: str
    title: Optional[str] = None
    lead: Optional[str] = None
    article: Optional[str] = None
    domain: Optional[str] = None
    url: Optional[str] = None
    date_of_creation: Optional[str] = datetime.datetime.now().strftime(
        "%Y-%m-%dT%H:%M:%S"
    )
    tags: Optional[list[str]] = None
