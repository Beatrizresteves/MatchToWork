import psycopg2
from abc import abstractmethod
from typing import List
from config import Config
from models.user import User

class IRepository:
  def __init__(self) -> None:
    pass

  @abstractmethod
  def get_users(self, limit: int, offset: int) -> List[User]:
    pass


class Repository(IRepository):
  def __init__(self):
    self.conn = psycopg2.connect(
        dbname=Config.DB_NAME,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        host=Config.DB_HOST,
        port=Config.DB_PORT,
    )

  def get_users(self, limit: int, offset: int) -> List[User]:
    conn = self.__get_connection()
    cur = conn.cursor()

    query = """
    SELECT
      user_id,
      username,
      email,
      fullname,
      cpf,
      phone_number,
      address_id,
      created_at,
      updated_at,
      is_active
    FROM users LIMIT %s OFFSET %s
    """

    cur.execute(query, (limit, offset))
    rows = cur.fetchall()
    users = [User.from_db_row(row) for row in rows]
    conn.close()

    return users

  def __get_connection(self):
    return psycopg2.connect(
        dbname=Config.DB_NAME,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        host=Config.DB_HOST,
        port=Config.DB_PORT,
    )
