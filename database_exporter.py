from prometheus_client import start_http_server, Gauge, Counter
import time
import logging
import psycopg2
import psycopg2.extras

def get_db_connection():
    """Установка подключения к PostgreSQL"""
    try:
        conn = psycopg2.connect(
            host="postgres",
            port="5432",  # ВНУТРИ Docker сети используется порт 5432
            database="postgres",
            user="postgres",  # Используем postgres вместо user
            password="user"
        )
        return conn
    except Exception as e:
        logging.error(f"❌ Ошибка подключения к БД: {e}")
        return None

# Метрики для базы данных
db_size = Gauge('pg_database_size_bytes', 'Database size in bytes', ['datname'])
db_connections = Gauge('pg_stat_activity_count', 'Active connections', ['datname', 'state'])
db_queries = Counter('pg_stat_database_tup_returned_total', 'Tuples returned', ['datname'])
db_inserts = Counter('pg_stat_database_tup_inserted_total', 'Tuples inserted', ['datname'])
db_updates = Counter('pg_stat_database_tup_updated_total', 'Tuples updated', ['datname'])
db_deletes = Counter('pg_stat_database_tup_deleted_total', 'Tuples deleted', ['datname'])
db_cache_hit = Gauge('pg_stat_database_blks_hit', 'Cache hits', ['datname'])
db_cache_miss = Gauge('pg_stat_database_blks_read', 'Cache misses', ['datname'])
db_uptime = Gauge('pg_postmaster_start_time_seconds', 'Postmaster start time')

def collect_real_metrics():
    """Сбор реальных метрик из PostgreSQL"""
    conn = get_db_connection()
    if not conn:
        return
    
    try:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        # Размеры баз данных
        cursor.execute("""
            SELECT datname, pg_database_size(datname) as size 
            FROM pg_database 
            WHERE datistemplate = false
        """)
        for row in cursor.fetchall():
            db_size.labels(datname=row['datname']).set(row['size'])
        
        # Активные подключения по базам и статусам
        cursor.execute("""
            SELECT datname, state, COUNT(*) as count 
            FROM pg_stat_activity 
            WHERE datname IS NOT NULL
            GROUP BY datname, state
        """)
        for row in cursor.fetchall():
            db_connections.labels(datname=row['datname'], state=row['state']).set(row['count'])
        
        # Статистика по базам данных
        cursor.execute("""
            SELECT 
                datname,
                tup_returned,
                tup_inserted,
                tup_updated,
                tup_deleted,
                blks_hit,
                blks_read
            FROM pg_stat_database 
            WHERE datname IS NOT NULL
        """)
        for row in cursor.fetchall():
            db_name = row['datname']
            db_queries.labels(datname=db_name).inc(row['tup_returned'])
            db_inserts.labels(datname=db_name).inc(row['tup_inserted'])
            db_updates.labels(datname=db_name).inc(row['tup_updated'])
            db_deletes.labels(datname=db_name).inc(row['tup_deleted'])
            db_cache_hit.labels(datname=db_name).set(row['blks_hit'])
            db_cache_miss.labels(datname=db_name).set(row['blks_read'])
        
        # Время запуска PostgreSQL
        cursor.execute("SELECT EXTRACT(epoch FROM pg_postmaster_start_time()) as start_time")
        start_time = cursor.fetchone()['start_time']
        db_uptime.set(start_time)
        
        cursor.close()
        conn.close()
        
        logging.info("✅ Реальные метрики собраны успешно")
        
    except Exception as e:
        logging.error(f"❌ Ошибка сбора метрик: {e}")

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    start_http_server(9187)
    logging.info("📊 Database Exporter started on port 9187")
    
    while True:
        collect_real_metrics()
        time.sleep(30)