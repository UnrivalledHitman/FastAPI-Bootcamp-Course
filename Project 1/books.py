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
@app.get("/books")
async def show_all_books():
    return books


# Path parameters
@app.get("/books/{bookTitle}")
async def show_specific_book(bookTitle: str):
    for book in books:
        # casefold for making the search case insensitive
        if book["title"].casefold() == bookTitle.casefold():
            return book
    # If the loop finishes without returning, the book doesn't exist
    raise HTTPException(status_code=404, detail="Book not found")


# Query parameters
@app.get("/books/")
async def display_book_category_wise(category: str):
    booksToReturn = []
    for book in books:
        if book.get("category", "").casefold() == category.casefold():
            booksToReturn.append(book)

    # Check if the list is empty
    if not booksToReturn:
        raise HTTPException(
            status_code=404, detail=f"No books found for category: '{category}'"
        )

    return booksToReturn


# Combining path and query parameters
@app.get("/books/{bookAuthor}/")
async def display_books_author_and_category_wise(bookAuthor: str, category: str):
    booksToReturn = []
    for book in books:
        if (
            book.get("author", "").casefold() == bookAuthor.casefold()
            and book.get("category", "").casefold() == category.casefold()
        ):
            booksToReturn.append(book)
    # Check if the list is empty
    if not booksToReturn:
        raise HTTPException(
            status_code=404,
            detail=f"No books found for author '{bookAuthor}' in category '{category}'",
        )

    return booksToReturn
