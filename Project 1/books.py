from fastapi import FastAPI
from fastapi import FastAPI, HTTPException

# Data
books = [
    {"title": "Title One", "author": "Author One", "category": "Science"},
    {"title": "Title Two", "author": "Author Two", "category": "Science"},
    {"title": "Title Three", "author": "Author Three", "category": "History"},
    {"title": "Title Four", "author": "Author Four", "category": "Math"},
    {"title": "Title Five", "author": "Author Five", "category": "Math"},
]

# Initializing fastapi
app = FastAPI()


# Showing all the books
@app.get("/")
async def show_all_books():
    return books


@app.get("/{book_title}")
async def show_specific_book(book_title: str):
    for book in books:
        # casefold for making the search case insensitive
        if book["title"].casefold() == book_title.casefold():
            return book

    # If the loop finishes without returning, the book doesn't exist
    raise HTTPException(status_code=404, detail="Book not found")
