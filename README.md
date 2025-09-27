# E-commerce Olist

![Project Banner](https://github.com/Nurkens/e-commerce-olist/blob/main/erdVis1.png) 

## Описание

**E-commerce Olist** — это проект, посвященный анализу и визуализации данных крупнейшей бразильской электронной коммерции Olist.  
В проекте используются современные инструменты анализа данных на Python.

## Возможности

- Анализ пользовательского поведения
- Визуализация ключевых метрик продаж
- Модели прогнозирования и кластеризации
- Гибкая архитектура для расширения

## Технологии

- Python
- Postgresql
-

## Установка

```bash
git clone https://github.com/Nurkens/e-commerce-olist.git
cd e-commerce-olist
pip install -r requirements.txt
```

## Как запустить

1. Установить зависимости:

pip install -r requirements.txt

Настроить переменные окружения в .env:

DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
DB_NAME=

Создать таблицы и загрузить данные:

psql -U postgres -d dataVis -p 5433 -f database/create_tables.sql
psql -U postgres -d dataVis -p 5433 -f database/import_data.sql

## Структура проекта

```
e-commerce-olist/
├── data/            # Датасеты
├── scripts/       # Jupyter Notebooks
├── database/             # Исходный код
├── requirements.txt # Зависимости
└── README.md
```

## Контакты

- Автор: [Nurkens](https://github.com/Nurkens)
- 

---
