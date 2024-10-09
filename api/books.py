import uvicorn
from fastapi import FastAPI

from api.data import BOOKS

app = FastAPI(title="My Books API")


@app.get("/books")
async def get_all_books():
    BOOKS.sort(key=lambda b: _get_author_last_name(b["author"]))
    return BOOKS


@app.get("/books/{isbn}")
async def get_book(isbn: str):
    return [b for b in BOOKS if b.get("isbn") == isbn]


def _get_author_last_name(name: str) -> str:
    return name.split()[-1]


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
