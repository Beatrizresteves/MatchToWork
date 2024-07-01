import psycopg2
from config import Config

def get_db_connection():
    conn = psycopg2.connect(
        dbname=Config.DB_NAME,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        host=Config.DB_HOST,
        port=Config.DB_PORT,
    )
    return conn

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id SERIAL PRIMARY KEY,
            username VARCHAR(80) NOT NULL,
            email VARCHAR(80) NOT NULL,
            password VARCHAR(128) NOT NULL,
            fullname VARCHAR(80) NOT NULL,
            cpf VARCHAR(11) NOT NULL,
            phone_number VARCHAR(15) NOT NULL,
            address_id INTEGER,
            created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
            update_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT TRUE
        );
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS servicetypes (
            service_type_id SERIAL PRIMARY KEY,
            name VARCHAR(80) NOT NULL,
            description VARCHAR(200),
            created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
            update_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
        );
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS services (
            service_id SERIAL PRIMARY KEY,
            service_type_id INTEGER NOT NULL,
            client_id INTEGER NOT NULL,
            start_date TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
            end_date TIMESTAMPTZ,
            status VARCHAR(20) NOT NULL,
            created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
            update_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (service_type_id) REFERENCES servicetypes (service_type_id),
            FOREIGN KEY (client_id) REFERENCES users (user_id)
        );
        CREATE INDEX IF NOT EXISTS idx_service_start_date ON services (start_date);
        CREATE INDEX IF NOT EXISTS idx_service_end_date ON services (end_date);
    ''')

    cur.execute('''
        CREATE OR REPLACE FUNCTION update_update_at_column()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.update_at = NOW();
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    ''')

    cur.execute('''
        CREATE TRIGGER update_users_update_at
        BEFORE UPDATE ON users
        FOR EACH ROW
        EXECUTE FUNCTION update_update_at_column();
    ''')

    cur.execute('''
        CREATE TRIGGER update_servicetypes_update_at
        BEFORE UPDATE ON servicetypes
        FOR EACH ROW
        EXECUTE FUNCTION update_update_at_column();
    ''')

    cur.execute('''
        CREATE TRIGGER update_services_update_at
        BEFORE UPDATE ON services
        FOR EACH ROW
        EXECUTE FUNCTION update_update_at_column();
    ''')

    conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':
    init_db()
