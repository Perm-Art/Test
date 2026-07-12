from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db import models
from app.schemas import BookCreate, BookResponse, BookUpdate
from app.db.db import get_db

router = APIRouter(prefix="/books", tags=["books"])

@router.get("/", response_model=List[BookResponse])
def read_books(
    db: Session = Depends(get_db),
    category_id: Optional[int] = Query(None, description="Фильтр по ID категории")
):
    """Получить список всех книг, с возможностью фильтрации по категории"""
    query = db.query(models.Book)
    if category_id:
        query = query.filter(models.Book.category_id == category_id)
    
    books = query.join(models.Category, models.Book.category_id == models.Category.id).add_columns(
        models.Category.title.label("category_title")
    ).all()
    
    result = []
    for book, category_title in books:
        book_dict = book.__dict__.copy()
        book_dict['category_title'] = category_title
        result.append(book_dict)
    return result

@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    """Создать новую книгу"""
    category = db.query(models.Category).filter(models.Category.id == book.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    new_book = models.Book(**book.model_dump())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    
    book_dict = new_book.__dict__.copy()
    book_dict['category_title'] = category.title
    return book_dict

@router.get("/{book_id}", response_model=BookResponse)
def read_book(book_id: int, db: Session = Depends(get_db)):
    """Получить книгу по ID"""
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    book_dict = book.__dict__.copy()
    book_dict['category_title'] = book.category.title if book.category else None
    return book_dict

@router.put("/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book_update: BookUpdate, db: Session = Depends(get_db)):
    """Обновить книгу по ID"""
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    update_data = book_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_book, key, value)
    
    db.commit()
    db.refresh(db_book)
    
    book_dict = db_book.__dict__.copy()
    book_dict['category_title'] = db_book.category.title if db_book.category else None
    return book_dict

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """Удалить книгу по ID"""
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(db_book)
    db.commit()
    return None