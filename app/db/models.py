# app/db/models.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Category(Base):
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, unique=True)
    
    books = relationship("Book", back_populates="category", cascade="all, delete-orphan")

class Book(Base):
    __tablename__ = 'books'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    url = Column(String(500), nullable=True, default='')
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    
    category = relationship("Category", back_populates="books")