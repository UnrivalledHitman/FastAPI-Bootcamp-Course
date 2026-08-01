from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, Field
from typing import Optional
from starlette import status

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    id: Optional[int] = Field(description="ID is not needed on create", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=3)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=6)
    published_date: int = Field(gt=999, lt=10000)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "NewBook",
                "author": "NewAuthor",
                "description": "NewDescription",
                "rating": 5,
                "published_date": 2012,
            }
        }
    }


books = [
    Book(
        id=1,
        title="The Martian",
        author="Andy Weir",
        description="An astronaut becomes stranded on Mars and must use his ingenuity to survive.",
        rating=5,
        published_date=2011,
    ),
    Book(
        id=2,
        title="1984",
        author="George Orwell",
        description="A dystopian social science fiction novel exploring totalitarianism and surveillance.",
        rating=4,
        published_date=1949,
    ),
    Book(
        id=3,
        title="The Hobbit",
        author="J.R.R. Tolkien",
        description="A peace-loving hobbit sets off on an epic adventure to reclaim a stolen dwarf kingdom.",
        rating=5,
        published_date=1937,
    ),
    Book(
        id=4,
        title="Atomic Habits",
        author="James Clear",
        description="A practical guide on how to build good habits and break bad ones.",
        rating=5,
        published_date=2018,
    ),
    Book(
        id=5,
        title="Pride and Prejudice",
        author="Jane Austen",
        description="A classic romance novel that tackles issues of manners, upbringing, and morality.",
        rating=4,
        published_date=1813,
    ),
]


# ---------- READ ----------


# This must be declared BEFORE /books/{bookID} to avoid route conflicts.
@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_book_by_rating(bookRating: int = Query(gt=-1, lt=6)):
    booksToReturn = []
    for book in books:
        if book.rating == bookRating:
            booksToReturn.append(book)
    return booksToReturn


# This must ALSO be declared BEFORE /books/{bookID} to avoid route conflicts,
# and it needs a distinct path from read_book_by_rating since both are under /books/.
@app.get("/books/publish/", status_code=status.HTTP_200_OK)
async def read_book_by_publish_date(published_date: int = Query(gt=999, lt=10000)):
    booksToReturn = []
    for book in books:
        if book.published_date == published_date:
            booksToReturn.append(book)
    return booksToReturn


@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return books


@app.get("/books/{bookID}", status_code=status.HTTP_200_OK)
async def read_book(bookID: int = Path(gt=0)):
    for book in books:
        if book.id == bookID:
            return book
    raise HTTPException(status_code=404, detail="Item not found")


# ---------- CREATE ----------


def find_book_id(book: Book):
    book.id = 1 if len(books) == 0 else books[-1].id + 1
    return book


@app.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    books.append(find_book_id(new_book))
    return new_book


# ---------- UPDATE ----------


@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    for i in range(len(books)):
        if books[i].id == book.id:
            book_data = book.model_dump()
            books[i] = Book(**book_data)
            return
    raise HTTPException(status_code=404, detail="Item not found")


# ---------- DELETE ----------


@app.delete("/books/{bookID}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(bookID: int = Path(gt=0)):
    for i in range(len(books)):
        if books[i].id == bookID:
            books.pop(i)
            return
    raise HTTPException(status_code=404, detail="Item not found")
