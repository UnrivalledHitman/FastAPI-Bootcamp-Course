from fastapi import FastAPI, Body
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


class BookRequest(BaseModel):
    id: Optional[str] = None
    title: str = Field(min_length=3)
    author: str = Field(min_length=3)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=6)

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


books = [
    Book(
        id="001",
        title="The Martian",
        author="Andy Weir",
        description="An astronaut becomes stranded on Mars and must use his ingenuity to survive.",
        rating=5,
    ),
    Book(
        id="002",
        title="1984",
        author="George Orwell",
        description="A dystopian social science fiction novel exploring totalitarianism and surveillance.",
        rating=4,
    ),
    Book(
        id="003",
        title="The Hobbit",
        author="J.R.R. Tolkien",
        description="A peace-loving hobbit sets off on an epic adventure to reclaim a stolen dwarf kingdom.",
        rating=5,
    ),
    Book(
        id="004",
        title="Atomic Habits",
        author="James Clear",
        description="A practical guide on how to build good habits and break bad ones.",
        rating=5,
    ),
    Book(
        id="005",
        title="Pride and Prejudice",
        author="Jane Austen",
        description="A classic romance novel that tackles issues of manners, upbringing, and morality.",
        rating=4,
    ),
]


@app.get("/books")
async def read_all_books():
    return books


@app.post("/create-book")
async def create_book(book_request: BookRequest):
    newBook = Book(**book_request.model_dump())
    books.append(newBook)


def find_book_id(book: Book):
    book.id = 1 if len(books) == 0 else books[-1].id + 1
    return book
