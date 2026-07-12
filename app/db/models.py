from .db import db

def create_tables():
    """Создает таблицы в БД, если они не существуют"""
    with db.get_cursor() as cur:
        # Создаем таблицу categories
        cur.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL UNIQUE
            );
        """)
        
        # Создаем таблицу books
        cur.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                price DECIMAL(10, 2) NOT NULL,
                url VARCHAR(500) DEFAULT '',
                category_id INTEGER REFERENCES categories(id) ON DELETE CASCADE
            );
        """)
        
        print("Таблицы успешно созданы (или уже существуют)")

def drop_tables():
    """Удаляет все таблицы"""
    with db.get_cursor() as cur:
        cur.execute("DROP TABLE IF EXISTS books CASCADE;")
        cur.execute("DROP TABLE IF EXISTS categories CASCADE;")
        print("Таблицы удалены")