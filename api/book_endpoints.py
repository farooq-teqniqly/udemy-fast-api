from typing import Optional

import uvicorn
from fastapi import Depends, FastAPI
from pydantic import BaseModel

import api.book_service as bs

app = FastAPI(title="My Books API")


class BookQueryParameters(BaseModel):
    author: Optional[str] = None
    category: Optional[str] = None
    top: Optional[int] = None
    isbn: Optional[str] = None


@app.get("/books/q")
async def query_book(params: BookQueryParameters = Depends()):
    return await bs.query_book(
        author=params.author, category=params.category, top=params.top, isbn=params.isbn
    )


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
