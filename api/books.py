from fastapi import FastAPI

app = FastAPI()

BOOKS = [
    dict(title="Foo", author="Bar", category="Science"),
    dict(title="The Great Gatsby", author="F. Scott Fitzgerald", category="Fiction"),
    dict(title="1984", author="George Orwell", category="Dystopian"),
    dict(title="To Kill a Mockingbird", author="Harper Lee", category="Classic"),
    dict(title="A Brief History of Time", author="Stephen Hawking", category="Science"),
    dict(title="The Catcher in the Rye", author="J.D. Salinger", category="Fiction"),
]


@app.get("/books")
async def get_all_books():
    return BOOKS
