import unittest
from typing import List
from models.user import User
from repository.user_repository import IRepository
from api.user_api import Endpoints

class MockRepository(IRepository):
    def __init__(self) -> None:
        super().__init__()
        self.users = [
            User(1, "luisnascimento", "luisnascimento@jcdecor.com.br", "123456", "Luís Nascimento", "12312314", "31 9182319"),
            User(2, "beatrizesteves", "beatrizesteves@jcdecor.com.br", "123456", "Beatriz Esteves", "12312314", "31 9182319"),
        ]

    def get_users(self, limit: int, offset: int) -> List[User]:
        return self.users[offset:offset + limit]
    
    def add_user(self, user: User) -> User:
        self.users.append(user)
        return user

    def patch_user(self, user: User) -> User:
        for i, existing_user in enumerate(self.users):
            if existing_user.id == user.id:
                self.users[i] = user
                return user
        raise ValueError("User not found")
    
class TestEndpoints(unittest.TestCase):
    def setUp(self):
        mock = MockRepository()
        self.endpoints = Endpoints(mock)

    def test_get_users(self):
        users, status = self.endpoints.get_users()

        expected = [
            User(1, "luisnascimento", "luisnascimento@jcdecor.com.br", "123456", "Luís Nascimento", "12312314", "31 9182319"),
            User(2, "beatrizesteves", "beatrizesteves@jcdecor.com.br", "123456", "Beatriz Esteves", "12312314", "31 9182319"),
        ]

        self.assertEqual(status, 200, "should return OK code")
        self.assertEqual(users, expected, "should return 2 users")
        
    def test_create_user(self):
      new_user =  User(3, "beatrizramalho", "beatrizramalho.esteves@gmail.com", "963852", "Beatriz Ramalho", "3399999", "33 9999999")
      user, status = self.endpoints.create_user(new_user)
      self.assertEqual(status, 201, "should return Created code")
      self.assertEqual(user, new_user, "should return the created user")
      self.assertIn(new_user, self.endpoints.repository.users, "new user should be in repository")
      
def test_patch_user(self):
        updated_user = User(2, "beatrizramalho", "beatrizramalho.esteves@gmail.com", "963852", "Beatriz Ramalho", "3399999", "33 9999999")
        user, status = self.endpoints.patch_user(updated_user)
        self.assertEqual(status, 200, "should return OK code")
        self.assertEqual(user, updated_user, "should return the updated user")
        
        repository_user = next((u for u in self.endpoints.repository.users if u.id == updated_user.id), None)
        self.assertIsNotNone(repository_user, "updated user should be in repository")
        self.assertEqual(repository_user, updated_user, "repository user should match updated user")
    
if __name__ == "__main__":
    unittest.main()
