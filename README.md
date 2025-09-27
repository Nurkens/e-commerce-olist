# Olist E-commerce Dataset

This repository contains the Olist E-commerce Dataset, a comprehensive collection of data from a Brazilian e-commerce platform. The dataset includes information about orders, customers, products, reviews, and more, making it ideal for data analysis and machine learning projects.

## Dataset Overview

The dataset is organized into several CSV files, each representing a different aspect of the e-commerce platform:

- `orders.csv`: Contains information about customer orders, including order ID, customer ID, order status, and timestamps.
- `customers.csv`: Contains customer details such as customer ID, name, and location.
- `products.csv`: Contains product information including product ID, category, and price.
- `order_items.csv`: Contains details about the items in each order, including product ID,
  order ID, quantity, and price.

- `order_payments.csv`: Contains payment information for each order, including payment type and amount.
- `order_reviews.csv`: Contains customer reviews for orders, including review score and comments.
- `sellers.csv`: Contains information about sellers, including seller ID and location.
- `geolocation.csv`: Contains geolocation data for customers and sellers, including zip codes and

## 🗂️ Структура проекта

dataVis1/
│
├── database/
│ ├── create_tables.sql # Создание таблиц с PK и FK
│ ├── import_data.sql # Импорт CSV в PostgreSQL
│ ├── queries.sql # 10 аналитических SQL-запросов
│
├── scripts/
│ ├── config.py # Подключение к БД через SQLAlchemy
│ ├── main.py # Выполнение всех запросов и сохранение в CSV
│ ├
│ ├
│
├── results/ # CSV с результатами запросов
│ ├── query_1.csv
│ ├── query_2.csv
│ └── ...
│
├── .env # Доступы к базе
├── requirements.txt # Зависимости проекта
└── README.md # Документация проекта

---

## ⚙️ Установка и запуск

1. Клонировать проект:
   ```bash
   git clone https://github.com/olist-analytics.git
   cd olist-analytics
   ```

Установить зависимости:

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

Запустить Python-аналитику:

python scripts/main.py

Используемые инструменты:

PostgreSQL (хранение данных)

SQLAlchemy (подключение к базе из Python)

Pandas (работа с результатами)

pgAdmin (работа с базой, ERD)

Python (автоматизация аналитики)

Автор
Сердаков Нуркен
