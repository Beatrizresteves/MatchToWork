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
    def update_service(self, service: Service) -> Service:
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
        )

    def get_services(self, limit: int, offset: int) -> List[Service]:
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
        conn.close()
        return services

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

    def update_service(self, service: Service) -> Service:
        conn = self.__get_connection()
        cur = conn.cursor()
        try:
            cur.execute('''
                UPDATE services
                SET service_type_id = %s, client_id = %s, start_date = %s, end_date = %s, status = %s
                WHERE service_id = %s
            ''', (service.service_type_id, service.client_id, service.start_date, service.end_date, service.status, service.service_id))
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