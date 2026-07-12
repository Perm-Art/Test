from db.db import db
from db.models import create_tables
from db.crud import CategoryCRUD, BookCRUD

def init_database():
    """Инициализирует БД и заполняет тестовыми данными"""
    print("Создание таблиц...")
    create_tables()
    
    print("\nДобавление категорий...")
    # Добавляем категории
    categories_data = ['Фантастика', 'Детективы']
    category_ids = []
    
    for cat_title in categories_data:
        # Проверяем, существует ли категория
        existing = CategoryCRUD.get_by_title(cat_title)
        if existing:
            print(f"Категория '{cat_title}' уже существует")
            category_ids.append(existing['id'])
        else:
            category = CategoryCRUD.create(cat_title)
            print(f"Добавлена категория: {cat_title} (ID: {category['id']})")
            category_ids.append(category['id'])
    
    print("\nДобавление книг...")
    # Книги для категории "Фантастика" (первая категория)
    books_fantasy = [
        ('Дюна', 'Научно-фантастический роман Фрэнка Герберта', 599.99, 'https://example.com/duna'),
        ('1984', 'Роман-антиутопия Джорджа Оруэлла', 399.99, 'https://example.com/1984'),
        ('Машина времени', 'Научно-фантастический роман Герберта Уэллса', 299.99, 'https://example.com/time_machine'),
        ('Солярис', 'Философский научно-фантастический роман Станислава Лема', 499.99, 'https://example.com/solaris')
    ]
    
    # Книги для категории "Детективы" (вторая категория)
    books_detective = [
        ('Убийство в Восточном экспрессе', 'Детективный роман Агаты Кристи', 449.99, 'https://example.com/orient_express'),
        ('Шерлок Холмс', 'Сборник рассказов о знаменитом сыщике', 529.99, 'https://example.com/holmes'),
        ('Тень ветра', 'Роман-загадка Карлоса Руиса Сафона', 379.99, 'https://example.com/wind_shadow')
    ]
    
    # Добавляем книги в фантастику
    for title, desc, price, url in books_fantasy:
        BookCRUD.create(title, desc, price, category_ids[0], url)
        print(f"Добавлена книга: {title}")
    
    # Добавляем книги в детективы
    for title, desc, price, url in books_detective:
        BookCRUD.create(title, desc, price, category_ids[1], url)
        print(f"Добавлена книга: {title}")
    
    print("\nИнициализация БД завершена!")

if __name__ == "__main__":
    init_database()
print('123')