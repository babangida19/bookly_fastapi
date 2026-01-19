from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from typing import List
app  = FastAPI()

class Book(BaseModel):
        id: int
        title: str
        author: str
        publisher: str
        published_date: str
        page_count: int
        language: str

class BookUpdateModel(BaseModel):
        
        title: str
        author: str
        publisher: str
   
        page_count: int
        language: str    

@app.get('/books', response_model= List[Book])
async def get_all_books():
    return books

@app.post("/books", status_code=status.HTTP_201_CREATED)
async def create_a_book(book_data:Book) -> dict:
    new_book = book_data.model_dump()
    books.append(new_book)
    return new_book

@app.get("/book/{book_id}")
async def get_book(book_id:int) -> dict:
    for book in books:
         if book["id"] == book_id:
              return book
        
    raise HTTPException(
              status_code=status.HTTP_404_NOT_FOUND,
                detail="Book is not found")

@app.patch("/book/{book_id}")
async def update_book(book_id:int, book_update_data: BookUpdateModel) -> dict:
    for book in books:
         if book['id'] == book_id:
              book["title"] = book_update_data.title
              book['publisher'] = book_update_data.publisher
              book['page_count'] = book_update_data.page_count
              book['language'] = book_update_data.language
              return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book is not found")

@app.delete("/book/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id:int) :
    for book in books:
         if book["id"] == book_id:
              books.remove(book)
              return{}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book is not found")
