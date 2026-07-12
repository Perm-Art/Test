from fastapi import FastAPI
from app.api.v1 import books, categories
from app.db import models
from app.db.db import engine

# Создаем таблицы, если их нет (для запуска)
# models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Book API",
    description="API для управления книгами и категориями",
    version="1.0.0"
)

# Подключаем роутеры
app.include_router(books.router, prefix="/api/v1")
app.include_router(categories.router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    """Проверка состояния сервиса"""
    return {"status": "alive"}

@app.get("/")
async def root():
    return {"message": "Welcome to Book API! Visit /docs for documentation"}

# Запуск: uvicorn app.main:app --reload

print("Hello, World!")
