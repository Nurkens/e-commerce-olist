-- 1. Просмотр первых 10 строк из таблицы заказов
SELECT * FROM olist_orders_dataset LIMIT 10;

-- 2. Заказы в статусе "delivered"
SELECT * FROM olist_orders_dataset 
WHERE order_status = 'delivered'
ORDER BY order_purchase_timestamp DESC;

-- 3. Количество заказов по статусам
SELECT order_status, COUNT(*) AS total_orders
FROM olist_orders_dataset
GROUP BY order_status
ORDER BY total_orders DESC;

-- 4. Среднее, минимальное и максимальное значение оплаты
SELECT 
    AVG(payment_value) AS avg_payment,
    MIN(payment_value) AS min_payment,
    MAX(payment_value) AS max_payment
FROM olist_order_payments_dataset;

-- 5. Количество уникальных покупателей
SELECT COUNT(DISTINCT customer_unique_id) AS total_customers
FROM olist_customers_dataset;

-- 6. Количество заказов по штатам (TOP-10)
SELECT c.customer_state, COUNT(*) AS orders_count
FROM olist_orders_dataset o
JOIN olist_customers_dataset c ON o.customer_id = c.customer_id
GROUP BY c.customer_state
ORDER BY orders_count DESC
LIMIT 10;

-- 7. Топ-10 продавцов по количеству товаров
SELECT seller_id, COUNT(*) AS total_items
FROM olist_order_items_dataset
GROUP BY seller_id
ORDER BY total_items DESC
LIMIT 10;

-- 8. Топ-8 категорий товаров по продажам
SELECT p.product_category_name, COUNT(*) AS total_sold
FROM olist_order_items_dataset oi
JOIN olist_products_dataset p ON oi.product_id = p.product_id
GROUP BY p.product_category_name
ORDER BY total_sold DESC
LIMIT 8;

-- 9. Средний рейтинг по категориям товаров
SELECT p.product_category_name, ROUND(AVG(r.review_score), 2) AS avg_rating
FROM olist_order_reviews_dataset r
JOIN olist_orders_dataset o ON r.order_id = o.order_id
JOIN olist_order_items_dataset oi ON o.order_id = oi.order_id
JOIN olist_products_dataset p ON oi.product_id = p.product_id
GROUP BY p.product_category_name
ORDER BY avg_rating DESC
LIMIT 10;

-- 10. Общая выручка по годам
SELECT EXTRACT(YEAR FROM o.order_purchase_timestamp) AS year,
       ROUND(SUM(pay.payment_value), 2) AS total_revenue
FROM olist_orders_dataset o
JOIN olist_order_payments_dataset pay ON o.order_id = pay.order_id
GROUP BY year
ORDER BY year;
