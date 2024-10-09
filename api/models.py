from typing import Optional

from pydantic import BaseModel


class BookQueryParameters(BaseModel):
    author: Optional[str] = None
    category: Optional[str] = None
    top: Optional[int] = None
    isbn: Optional[str] = None
