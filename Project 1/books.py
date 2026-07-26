from fastapi import FastAPI, Body, HTTPException

# Data
books = [
    {"title": "Title One", "author": "Author One", "category": "Science"},
    {"title": "Title Two", "author": "Author Two", "category": "Science"},
    {"title": "Title Three", "author": "Author Three", "category": "History"},
    {"title": "Title Four", "author": "Author Four", "category": "Math"},
    {"title": "Title Five", "author": "Author Five", "category": "Math"},
]

app = FastAPI()


# 1. COMBINED: Show all books OR filter by query parameters
# Replacing three separate GET "/books" routes
@app.get("/books")
async def get_books(authorName: str, category: str):
    books_to_return = books

    if authorName:
        books_to_return = [
            book
            for book in books_to_return
            if book.get("author", "").casefold() == authorName.casefold()
        ]

    if category:
        books_to_return = [
            book
            for book in books_to_return
            if book.get("category", "").casefold() == category.casefold()
        ]

    if not books_to_return:
        raise HTTPException(
            status_code=404, detail="No books found matching the criteria"
        )

    return books_to_return


# 2. Combining path and query parameters
@app.get("/books/by_author/{bookAuthor}/")
async def display_books_author_and_category_wise(bookAuthor: str, category: str):
    booksToReturn = []
    for book in books:
        if (
            book.get("author", "").casefold() == bookAuthor.casefold()
            and book.get("category", "").casefold() == category.casefold()
        ):
            booksToReturn.append(book)

    if not booksToReturn:
        raise HTTPException(
            status_code=404,
            detail=f"No books found for author '{bookAuthor}' in category '{category}'",
        )
    return booksToReturn


# 3. Path parameter for Author Name (FIXED PATH)
# /books/author/{authorName} changed to {bookTitle} to prevent conflict
@app.get("/books/author/{authorName}")
async def fetch_books_by_authors_path_param(authorName: str):
    fetchedBooks = []
    for book in books:
        if book.get("author", "").casefold() == authorName.casefold():
            fetchedBooks.append(book)

    if not fetchedBooks:
        raise HTTPException(status_code=404, detail="Author not found")
    return fetchedBooks


# 4. Path parameter for Book Title
@app.get("/books/{bookTitle}")
async def show_specific_book(bookTitle: str):
    for book in books:
        if book["title"].casefold() == bookTitle.casefold():
            return book
    raise HTTPException(status_code=404, detail="Book not found")


# 5. Adding book data
@app.post("/books/create_book")
async def create_new_book(new_book=Body()):
    books.append(new_book)
    return {"message": "Book added"}


# 6. Updating a book data
@app.put("/books/update_book")
async def update_book_data(updated_book=Body()):
    for i in range(len(books)):
        if (
            books[i].get("title", "").casefold()
            == updated_book.get("title", "").casefold()
        ):
            books[i] = updated_book
            return {"message": "Book updated"}
    raise HTTPException(status_code=404, detail="Book not found")


# 7. Delete a book data
@app.delete("/books/delete_book/{bookTitle}")
async def delete_book(bookTitle: str):
    for i in range(len(books)):
        if books[i].get("title", "").casefold() == bookTitle.casefold():
            books.pop(i)
            return {"message": "Book deleted"}
    raise HTTPException(status_code=404, detail="Book not found")
