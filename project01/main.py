from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel

app = FastAPI()

books = [{"title": "book1", "author": "author1"}, {"title": "book2", "author": "author2"},
         {"title": "book3", "author": "author3"}, {"title": "book4", "author": "author4"},
         {"title": "book5", "author": "author5"}, {"title": "book6", "author": "author6"}]


@app.get("/")
async def get_all_books():
    return books


@app.get("/book/{book_title}")
async def get_book_by_title(book_title: str) -> list[dict[str, str]]:
    """

    根据书籍标题获取书籍信息

    Args:
        book_title (str): 书籍标题
    Returns:
        list[dict[str, str]]: 包含书籍信息的字典列表，每个字典包含"title"和"author"键
    """
    matching_books = [book for book in books if book["title"].casefold() == book_title.casefold()]

    if not matching_books:
        raise HTTPException(status_code=404, detail="Book not found")

    return matching_books


class CreateBook(BaseModel):
    """
    创建新的书籍信息
    """
    title: str
    author: str


@app.post("/book/add_book/")
async def add_book(newbook: CreateBook = Body(description="New book to add")):
    """

    添加新的书籍信息

    Args:
        newbook CreateBook: 包含书籍信息的字典，包含"title"和"author"键
    Returns:
        dict[str, str]: 添加成功后的书籍信息
    """
    books.append(dict(newbook))
    return books


@app.put("/book/update_book/{book_title}")
async def update_book(book_title: str, updated_book: CreateBook = Body(description="update book")):
    """

    更新书籍信息

    Args:
        book_title (str): 书籍标题
        updated_book (dict[str, str]): 包含更新书籍信息的字典，包含"title"和"author"键
    Returns:
        dict[str, str]: 更新成功后的书籍信息
    """
    for index, book in enumerate(books):
        if book["title"].casefold() == book_title.casefold():
            books[index] = dict(updated_book)
            return books[index]
    raise HTTPException(status_code=404, detail="Book not found")


@app.delete("/book/delete_book/{book_title}")
async def delete_book_by_title(book_title: str):
    """

    删除书籍信息

    Args:
        book_title (str): 书籍标题

    """
    for index, book in enumerate(books):
        if book["title"].casefold() == book_title.casefold():
            del books[index]
