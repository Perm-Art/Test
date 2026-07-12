import psycopg2
from psycopg2 import sql, extras
from contextlib import contextmanager
import os
from dotenv import load_dotenv
# app/db/db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import get_db_url

# Создаем движок (синхронный)
DATABASE_URL = get_db_url()
engine = create_engine(DATABASE_URL, pool_pre_ping=True) # pool_pre_ping - полезно для проверки соединения
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Функция-зависимость для FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
load_dotenv()

#class Database:
#    def __init__(self):
#        self.host = os.getenv('DB_HOST', 'localhost')
#        self.port = os.getenv('DB_PORT', '5432')
#        self.database = os.getenv('DB_NAME', 'bookstore')
#        self.user = os.getenv('DB_USER', 'postgres')
#        self.password = os.getenv('DB_PASSWORD', 'postgres')
#    
#    def get_connection(self):
#        """Создает подключение к БД"""
#        try:
#            conn = psycopg2.connect(
#                host=self.host,
#                port=self.port,
#                database=self.database,
#                user=self.user,
#                password=self.password
#            )
#            return conn
#        except Exception as e:
#            print(f"Ошибка подключения к БД: {e}")
#            raise
#   
#    @contextmanager
#    def get_cursor(self):
#        """Контекстный менеджер для работы с курсором"""
#        conn = self.get_connection()
#        try:
#           with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
#                yield cur
#                conn.commit()
#        except Exception as e:
#            conn.rollback()
#            print(f"Ошибка выполнения запроса: {e}")
#            raise
#        finally:
#            conn.close()

# Создаем экземпляр БД
#db = Database()