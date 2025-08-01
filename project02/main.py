from fastapi import FastAPI, Body, Path
from pydantic import BaseModel, Field
from typing import List

from starlette.exceptions import HTTPException

app = FastAPI()

BOOKS = [{"book_id": 1, "book_title": "book1", "book_author": "author1", "book_description": "description1",
          "book_rating": 1},
         {"book_id": 2, "book_title": "book2", "book_author": "author2", "book_description": "description2",
          "book_rating": 2},
         {"book_id": 3, "book_title": "book3", "book_author": "author3", "book_description": "description3",
          "book_rating": 3},
         {"book_id": 4, "book_title": "book4", "book_author": "author4", "book_description": "description4",
          "book_rating": 4},
         {"book_id": 5, "book_title": "book5", "book_author": "author5", "book_description": "description5",
          "book_rating": 5}]


class CreateBook(BaseModel):
    book_id: int | None = Field(default=None, exclude=True)
    book_title: str = Field(max_length=50)
    book_author: str = Field(max_length=50)
    book_description: str = Field(max_length=100)
    book_rating: int = Field(ge=0, le=5)

    model_config = {
        "json_schema_extra": {
            "example": {
                "book_title": "new book",
                "book_author": "new book author",
                "book_description": "new book description",
                "book_rating": 1
            }
        }
    }


@app.get("/book/")
async def get_all_books():
    return BOOKS


@app.get("/book/{book_id}")
async def get_book_by_id(book_id: int):
    return next((book for book in BOOKS if book_id == book["book_id"]), {"data": "book not found"})


@app.post("/book/add_book/")
async def add_book(new_book: CreateBook = Body(description="New book to add")):
    new_book = new_book.model_dump()
    if BOOKS:
        new_book["book_id"] = BOOKS[-1]["book_id"] + 1
    else:
        new_book["book_id"] = 1
    BOOKS.append(new_book)
    return {"data": "book added"}


class UpdateBook(BaseModel):
    book_title: str | None = Field(default=None, max_length=50)
    book_author: str | None = Field(default=None, max_length=50)
    book_description: str | None = Field(default=None, max_length=100)
    book_rating: int | None = Field(default=None, ge=0, le=5)
    model_config = {
        "json_schema_extra": {
            "example": {
                "book_title": "new book",
                "book_author": "new book author",
                "book_description": "new book description",
                "book_rating": 1
            }
        }
    }


@app.put("/book/update_book/{book_id}")
async def update_book(book_id: int = Path(gt=0), updated_book: UpdateBook = Body(description="Updated book")):
    for book in BOOKS:
        if book_id == book["book_id"]:
            book.update(updated_book.model_dump())
            return {"data": "book updated"}
    raise HTTPException(status_code=404, detail="Book not found")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8001)
