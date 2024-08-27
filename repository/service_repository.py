import psycopg2
from abc import abstractmethod
from typing import List
from config import Config
from models.service import Service

class IServiceRepository:
    def __init__(self) -> None:
        pass

    @abstractmethod
    def get_services(self, limit: int, offset: int) -> List[Service]:
        pass
    
    @abstractmethod
    def get_service(self, service_id: int) -> Service:
        pass
    
    @abstractmethod
    def add_service(self, service: Service) -> Service:
        pass
    
    @abstractmethod
    def patch_service(self, service: Service) -> Service:
        pass
    
    @abstractmethod
    def put_service(self, service: Service) -> Service:
        pass
    
    @abstractmethod
    def delete_service(self, service_id: int) -> bool:
        pass

class ServiceRepository(IServiceRepository):
    def __init__(self):
        self.conn = psycopg2.connect(
        dbname=Config.DB_NAME,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        options="-c client_encoding=UTF8"
    )

    def get_services(self, limit: int, offset: int) -> List[Service]:
        conn = None
        try:
            conn = self.__get_connection()
            cur = conn.cursor()
            query = """
            SELECT
            service_id,
            service_type_id,
            client_id,
            start_date,
            end_date,
            status,
            updated_at,
            created_at,
            is_active
            FROM services
            LIMIT %s OFFSET %s
            """
            cur.execute(query, (limit, offset))
            rows = cur.fetchall()
            services = [Service.from_db_row(row) for row in rows]
            return services
        except Exception as e:
            print(f"Erro ao obter serviços: {e}")
            raise e
        finally:
            if conn:
                conn.close()

    def get_service(self, service_id: int) -> Service:
        conn = self.__get_connection()
        cur = conn.cursor()
        query = """
        SELECT
          service_id,
          service_type_id,
          client_id,
          start_date,
          end_date,
          status,
          updated_at,
          created_at,
          is_active
        FROM services
        WHERE service_id = %s
        """
        cur.execute(query, (service_id,))
        row = cur.fetchone()
        conn.close()
        if row:
            return Service.from_db_row(row)
        else:
            raise ValueError("Service not found")

    def add_service(self, service: Service) -> Service:
        conn = self.__get_connection()
        cur = conn.cursor()
        try:
            cur.execute('''
                INSERT INTO services (service_type_id, client_id, start_date, end_date, status)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING service_id
            ''', (service.service_type_id, service.client_id, service.start_date, service.end_date, service.status))
            service.service_id = cur.fetchone()[0]
            conn.commit()
            conn.close()
            return service
        except Exception as e:
            conn.rollback()
            conn.close()
            raise e

    def put_service(self, service: Service) -> Service:
        conn = self.__get_connection()
        cur = conn.cursor()
        try:
            cur.execute('''
                INSERT INTO services (service_id, service_type_id, client_id, start_date, end_date, status)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (service_id) 
                DO UPDATE SET
                    service_type_id = EXCLUDED.service_type_id,
                    client_id = EXCLUDED.client_id,
                    start_date = EXCLUDED.start_date,
                    end_date = EXCLUDED.end_date,
                    status = EXCLUDED.status
                RETURNING service_id
            ''', (service.service_id, service.service_type_id, service.client_id, service.start_date, service.end_date, service.status))
            conn.commit()
            cur.execute('SELECT * FROM services WHERE service_id = %s', (service.service_id,))
            updated_service = Service.from_db_row(cur.fetchone())
            conn.close()
            return updated_service
        except Exception as e:
            conn.rollback()
            conn.close()
            raise e

    def patch_service(self, service: Service) -> Service:
        conn = self.__get_connection()
        cur = conn.cursor()
        try:
            updates = []
            params = []
            if service.service_type_id is not None:
                updates.append("service_type_id = %s")
                params.append(service.service_type_id)
            if service.client_id is not None:
                updates.append("client_id = %s")
                params.append(service.client_id)
            if service.start_date is not None:
                updates.append("start_date = %s")
                params.append(service.start_date)
            if service.end_date is not None:
                updates.append("end_date = %s")
                params.append(service.end_date)
            if service.status is not None:
                updates.append("status = %s")
                params.append(service.status)
            
            if not updates:
                raise ValueError("No fields to update")
            
            query = f'''
                UPDATE services
                SET {', '.join(updates)}
                WHERE service_id = %s
                RETURNING service_id
            '''
            params.append(service.service_id)
            cur.execute(query, params)
            conn.commit()
            cur.execute('SELECT * FROM services WHERE service_id = %s', (service.service_id,))
            updated_service = Service.from_db_row(cur.fetchone())
            conn.close()
            return updated_service
        except Exception as e:
            conn.rollback()
            conn.close()
            raise e

    def delete_service(self, service_id: int) -> bool:
        conn = self.__get_connection()
        cur = conn.cursor()
        try:
            cur.execute('DELETE FROM services WHERE service_id = %s', (service_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            conn.rollback()
            conn.close()
            raise e

    def __get_connection(self):
        return psycopg2.connect(
            dbname=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            host=Config.DB_HOST,
            port=Config.DB_PORT,
        )