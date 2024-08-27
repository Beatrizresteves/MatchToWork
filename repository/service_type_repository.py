import psycopg2
from abc import abstractmethod
from typing import List
from config import Config
from models.servicetype import ServiceType

class IServiceTypeRepository:
    def __init__(self) -> None:
        pass

    @abstractmethod
    def get_service_types(self, limit: int, offset: int) -> List[ServiceType]:
        pass
    
    @abstractmethod
    def get_service_type(self, service_type_id: int) -> ServiceType:
        pass
    
    @abstractmethod
    def add_service_type(self, service_type: ServiceType) -> ServiceType:
        pass
    
    @abstractmethod
    def patch_service_type(self, service_type: ServiceType) -> ServiceType:
        pass
    
    @abstractmethod
    def put_service_type(self, service_type: ServiceType) -> ServiceType:
        pass
    
    @abstractmethod
    def delete_service_type(self, service_type_id: int) -> bool:
        pass

class ServiceTypeRepository(IServiceTypeRepository):
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            options="-c client_encoding=UTF8"
        )

    def get_service_types(self, limit: int, offset: int) -> List[ServiceType]:
        conn = None
        try:
            conn = self.__get_connection()
            cur = conn.cursor()
            query = """
            SELECT
                service_type_id,
                name,
                description,
                updated_at,
                is_active
            FROM servicetypes
            LIMIT %s OFFSET %s
            """
            cur.execute(query, (limit, offset))
            rows = cur.fetchall()
            service_types = [ServiceType.from_db_row(row) for row in rows]
            return service_types
        except Exception as e:
            print(f"Erro ao obter tipos de serviço: {e}")
            raise e
        finally:
            if conn:
                conn.close()

    def get_service_type(self, service_type_id: int) -> ServiceType:
        conn = self.__get_connection()
        cur = conn.cursor()
        query = """
        SELECT
            service_type_id,
            name,
            description,
            updated_at,
            is_active
        FROM servicetypes
        WHERE service_type_id = %s
        """
        cur.execute(query, (service_type_id,))
        row = cur.fetchone()
        conn.close()
        if row:
            return ServiceType.from_db_row(row)
        else:
            raise ValueError("ServiceType not found")

    def add_service_type(self, service_type: ServiceType) -> ServiceType:
        conn = self.__get_connection()
        cur = conn.cursor()
        try:
            cur.execute('''
                INSERT INTO servicetypes (name, description)
                VALUES (%s, %s)
                RETURNING service_type_id
            ''', (service_type.name, service_type.description))
            service_type.service_type_id = cur.fetchone()[0]
            conn.commit()
            conn.close()
            return service_type
        except Exception as e:
            conn.rollback()
            conn.close()
            raise e

    def put_service_type(self, service_type: ServiceType) -> ServiceType:
        conn = self.__get_connection()
        cur = conn.cursor()
        try:
            cur.execute('''
                INSERT INTO servicetypes (service_type_id, name, description)
                VALUES (%s, %s, %s)
                ON CONFLICT (service_type_id) 
                DO UPDATE SET
                    name = EXCLUDED.name,
                    description = EXCLUDED.description
                RETURNING service_type_id
            ''', (service_type.service_type_id, service_type.name, service_type.description))
            conn.commit()
            cur.execute('SELECT * FROM servicetypes WHERE service_type_id = %s', (service_type.service_type_id,))
            updated_service_type = ServiceType.from_db_row(cur.fetchone())
            conn.close()
            return updated_service_type
        except Exception as e:
            conn.rollback()
            conn.close()
            raise e

    def patch_service_type(self, service_type: ServiceType) -> ServiceType:
        conn = self.__get_connection()
        cur = conn.cursor()
        try:
            updates = []
            params = []
            if service_type.name is not None:
                updates.append("name = %s")
                params.append(service_type.name)
            if service_type.description is not None:
                updates.append("description = %s")
                params.append(service_type.description)
            
            if not updates:
                raise ValueError("No fields to update")
            
            query = f'''
                UPDATE servicetypes
                SET {', '.join(updates)}
                WHERE service_type_id = %s
                RETURNING service_type_id
            '''
            params.append(service_type.service_type_id)
            cur.execute(query, params)
            conn.commit()
            cur.execute('SELECT * FROM servicetypes WHERE service_type_id = %s', (service_type.service_type_id,))
            updated_service_type = ServiceType.from_db_row(cur.fetchone())
            conn.close()
            return updated_service_type
        except Exception as e:
            conn.rollback()
            conn.close()
            raise e

    def delete_service_type(self, service_type_id: int) -> bool:
        conn = self.__get_connection()
        cur = conn.cursor()
        try:
            cur.execute('DELETE FROM servicetypes WHERE service_type_id = %s', (service_type_id,))
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
