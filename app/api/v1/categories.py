from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db import models
from app.schemas import CategoryCreate, CategoryResponse, CategoryUpdate
from app.db.db import get_db

router = APIRouter(prefix="/categories", tags=["categories"])

@router.get("/", response_model=List[CategoryResponse])
def read_categories(db: Session = Depends(get_db)):
    """Получить список всех категорий"""
    return db.query(models.Category).all()

@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    """Создать новую категорию"""
    db_category = db.query(models.Category).filter(models.Category.title == category.title).first()
    if db_category:
        raise HTTPException(status_code=400, detail="Category already exists")
    new_category = models.Category(title=category.title)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(category_id: int, category_update: CategoryUpdate, db: Session = Depends(get_db)):
    """Обновить категорию по ID"""
    db_category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    if category_update.title:
        existing = db.query(models.Category).filter(models.Category.title == category_update.title).first()
        if existing and existing.id != category_id:
            raise HTTPException(status_code=400, detail="Category with this title already exists")
        db_category.title = category_update.title
    
    db.commit()
    db.refresh(db_category)
    return db_category

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    """Удалить категорию по ID"""
    db_category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(db_category)
    db.commit()
    return None