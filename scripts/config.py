import os
import pandas as pd
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

def get_db_connection():
    """Создание подключения к PostgreSQL через SQLAlchemy"""
    try:
        user = os.getenv("DB_USER", "postgres")
        password = os.getenv("DB_PASSWORD", "user")
        host = os.getenv("DB_HOST", "localhost")
        port = os.getenv("DB_PORT", "5433")
        database = os.getenv("DB_NAME", "dataVis")

        connection_string = f"postgresql://{user}:{password}@{host}:{port}/{database}"
        engine = create_engine(connection_string)

        # Тестируем подключение
        with engine.connect() as conn:
            print("✅ Подключение к PostgreSQL успешно!")

        return engine
    except Exception as e:
        print(f"❌ Ошибка подключения к базе данных: {e}")
        return None

def execute_query(engine, query):
    """Выполнение SQL-запроса и возврат DataFrame"""
    try:
        df = pd.read_sql_query(query, engine)
        return df
    except Exception as e:
        print(f"❌ Ошибка выполнения запроса: {e}")
        return None

def get_table_names(engine):
    """Получить список всех таблиц в базе данных"""
    try:
        inspector = inspect(engine)
        return inspector.get_table_names()
    except Exception as e:
        print(f"❌ Ошибка получения списка таблиц: {e}")
        return []

def save_to_csv(df, filename):
    """Сохранить результат запроса в CSV"""
    if df is not None:
        df.to_csv(filename, index=False)
        print(f"💾 Результат сохранён в {filename}")
    else:
        print(f"⚠️ Пустой результат, файл {filename} не создан")
