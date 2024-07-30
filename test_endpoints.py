import unittest

from typing import List
from models.user import User
from repository.user_repository import Repository, IRepository
from api.user_api import Endpoints

class MockRepository(IRepository):
  def __init__(self) -> None:
    super().__init__()
  
  def get_users(self, limit: int, offset: int) -> List[User]:
    return [
      User(1, "luisnascimento", "luisnascimento@jcdecor.com.br", "123456", "Luís Nascimento", "12312314", "31 9182319"),
      User(1, "beatrizesteves", "beatrizesteves@jcdecor.com.br", "123456", "Beatriz Esteves", "12312314", "31 9182319"),
    ]
  
class TestEndpoints(unittest.TestCase):
  def setUp(self):
    mock = MockRepository()
    self.endpoints = Endpoints(mock)

  def test_get_users(self):
    users, status = self.endpoints.get_users()

    expected = [
      User(1, "luisnascimento", "luisnascimento@jcdecor.com.br", "123456", "Luís Nascimento", "12312314", "31 9182319"),
      User(1, "beatrizesteves", "beatrizesteves@jcdecor.com.br", "123456", "Beatriz Esteves", "12312314", "31 9182319"),
    ]

    self.assertEqual(status, 200, "should return OK code")
    self.assertEqual(users, expected, "should return 2 users")
