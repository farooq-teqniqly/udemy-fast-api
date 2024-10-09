import uvicorn
from fastapi import Depends, FastAPI

import api.book_service as bs
from api.models import BookQueryParameters

app = FastAPI(title="My Books API")


@app.get("/books/q")
async def query_book(params: BookQueryParameters = Depends()):
    return await bs.query_book(params)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
