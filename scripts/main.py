import os
from datetime import datetime
from config import get_db_connection, execute_query, save_to_csv

def run_queries(engine, queries_file="queries.sql"):
    """Выполнить все SQL-запросы из файла"""
    if not os.path.exists(queries_file):
        print(f"❌ Файл {queries_file} не найден")
        return

    with open(queries_file, "r", encoding="utf-8") as f:
        sql_script = f.read()

    # Разбиваем на отдельные запросы по точке с запятой
    queries = [q.strip() for q in sql_script.split(";") if q.strip()]

    results_dir = "results"
    os.makedirs(results_dir, exist_ok=True)

    for i, query in enumerate(queries, start=1):
        print(f"\n{'='*60}")
        print(f"▶️ Запрос {i}:")
        print(query[:200] + ("..." if len(query) > 200 else ""))  # показываем первые 200 символов запроса
        print(f"{'='*60}")

        df = execute_query(engine, query)
        if df is not None:
            print(df.head(10).to_string(index=False))  # печатаем первые 10 строк результата
            filename = os.path.join(results_dir, f"query_{i}.csv")
            save_to_csv(df, filename)
        else:
            print("⚠️ Ошибка или пустой результат")

def main():
    print(f"🛒 Olist E-Commerce Analytics")
    print(f"📊 Дата запуска: {datetime.now().strftime('%d.%m.%Y %H:%M')}")
    print("=" * 60)

    engine = get_db_connection()
    if not engine:
        print("❌ Не удалось подключиться к базе данных")
        return

    try:
        run_queries(engine, "database/queries.sql")

        print("\n" + "=" * 60)
        print("✅ Все запросы успешно выполнены и сохранены в папку results")
        print(f"📅 Завершено: {datetime.now().strftime('%d.%m.%Y %H:%M')}")
    except Exception as e:
        print(f"❌ Ошибка выполнения: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if engine:
            engine.dispose()
            print("🔒 Подключение к базе данных закрыто")

if __name__ == "__main__":
    main()
