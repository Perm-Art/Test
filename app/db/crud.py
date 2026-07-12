from .db import db
from psycopg2 import sql

# ============ CRUD для Categories ============

class CategoryCRUD:
    @staticmethod
    def create(title):
        """Создать категорию"""
        with db.get_cursor() as cur:
            cur.execute(
                "INSERT INTO categories (title) VALUES (%s) RETURNING id, title",
                (title,)
            )
            return cur.fetchone()
    
    @staticmethod
    def get_all():
        """Получить все категории"""
        with db.get_cursor() as cur:
            cur.execute("SELECT * FROM categories ORDER BY id")
            return cur.fetchall()
    
    @staticmethod
    def get_by_id(category_id):
        """Получить категорию по ID"""
        with db.get_cursor() as cur:
            cur.execute("SELECT * FROM categories WHERE id = %s", (category_id,))
            return cur.fetchone()
    
    @staticmethod
    def get_by_title(title):
        """Получить категорию по названию"""
        with db.get_cursor() as cur:
            cur.execute("SELECT * FROM categories WHERE title = %s", (title,))
            return cur.fetchone()
    
    @staticmethod
    def update(category_id, new_title):
        """Обновить категорию"""
        with db.get_cursor() as cur:
            cur.execute(
                "UPDATE categories SET title = %s WHERE id = %s RETURNING *",
                (new_title, category_id)
            )
            return cur.fetchone()
    
    @staticmethod
    def delete(category_id):
        """Удалить категорию"""
        with db.get_cursor() as cur:
            cur.execute("DELETE FROM categories WHERE id = %s RETURNING id", (category_id,))
            return cur.fetchone()

# ============ CRUD для Books ============

class BookCRUD:
    @staticmethod
    def create(title, description, price, category_id, url=''):
        """Создать книгу"""
        with db.get_cursor() as cur:
            cur.execute(
                """INSERT INTO books (title, description, price, category_id, url) 
                   VALUES (%s, %s, %s, %s, %s) RETURNING *""",
                (title, description, price, category_id, url)
            )
            return cur.fetchone()
    
    @staticmethod
    def get_all():
        """Получить все книги с информацией о категории"""
        with db.get_cursor() as cur:
            cur.execute("""
                SELECT b.*, c.title as category_title 
                FROM books b 
                LEFT JOIN categories c ON b.category_id = c.id 
                ORDER BY b.id
            """)
            return cur.fetchall()
    
    @staticmethod
    def get_by_id(book_id):
        """Получить книгу по ID"""
        with db.get_cursor() as cur:
            cur.execute("""
                SELECT b.*, c.title as category_title 
                FROM books b 
                LEFT JOIN categories c ON b.category_id = c.id 
                WHERE b.id = %s
            """, (book_id,))
            return cur.fetchone()
    
    @staticmethod
    def get_by_category(category_id):
        """Получить все книги категории"""
        with db.get_cursor() as cur:
            cur.execute("""
                SELECT b.*, c.title as category_title 
                FROM books b 
                LEFT JOIN categories c ON b.category_id = c.id 
                WHERE b.category_id = %s
            """, (category_id,))
            return cur.fetchall()
    
    @staticmethod
    def update(book_id, title=None, description=None, price=None, category_id=None, url=None):
        """Обновить книгу (обновляются только переданные поля)"""
        with db.get_cursor() as cur:
            updates = []
            params = []
            
            if title is not None:
                updates.append("title = %s")
                params.append(title)
            if description is not None:
                updates.append("description = %s")
                params.append(description)
            if price is not None:
                updates.append("price = %s")
                params.append(price)
            if category_id is not None:
                updates.append("category_id = %s")
                params.append(category_id)
            if url is not None:
                updates.append("url = %s")
                params.append(url)
            
            if not updates:
                return None
            
            params.append(book_id)
            query = sql.SQL("UPDATE books SET {} WHERE id = %s RETURNING *").format(
                sql.SQL(', ').join(map(sql.SQL, updates))
            )
            cur.execute(query, params)
            return cur.fetchone()
    
    @staticmethod
    def delete(book_id):
        """Удалить книгу"""
        with db.get_cursor() as cur:
            cur.execute("DELETE FROM books WHERE id = %s RETURNING id", (book_id,))
            return cur.fetchone()