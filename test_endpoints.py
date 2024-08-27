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
        for idx, u in enumerate(self.users):
            if u.user_id == user.user_id:
                if user.username is not None:
                    u.username = user.username
                if user.email is not None:
                    u.email = user.email
                if user.fullname is not None:
                    u.fullname = user.fullname
                if user.cpf is not None:
                    u.cpf = user.cpf
                if user.phone_number is not None:
                    u.phone_number = user.phone_number
                return u
        return None


    def put_user(self, user: User) -> User:
        for idx, u in enumerate(self.users):
            if u.user_id == user.user_id:
                self.users[idx] = user
                return user
        return None
    
    def delete_user(self, user_id: int) -> dict:
        user_to_delete = next((u for u in self.users if u.user_id == user_id), None)
        if user_to_delete:
            self.users.remove(user_to_delete)
            return {"message": "User deleted successfully"}
        else:
            return {"message": "User not found"}
    
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
        new_user = User(3, "beatrizramalho", "beatrizramalho.esteves@gmail.com", "963852", "Beatriz Ramalho", "3399999", "33 9999999")
        user, status = self.endpoints.create_user(new_user)
        self.assertEqual(status, 201, "should return Created code")
        self.assertEqual(user, new_user, "should return the created user")
        self.assertIn(new_user, self.endpoints.repository.users, "new user should be in repository")
      
    def test_patch_user(self):
        user = User(2, "beatrizramalho", "beatrizramalho.esteves@gmail.com", "963852", "Beatriz Ramalho", "3399999", "33 9999999")
        updated_user, status = self.endpoints.patch_user(user)
        self.assertEqual(status, 200, "should return OK code")
        self.assertEqual(updated_user, user, "should return the patched user")
        self.assertIn(updated_user, self.endpoints.repository.users, "patched user should be in repository")

    def test_put_user(self):
        user = User(2, "beatrizramalho", "beatrizramalho.esteves@gmail.com", "963852", "Beatriz Ramalho", "3399999", "33 9999999")
        updated_user, status = self.endpoints.put_user(user)
        self.assertEqual(status, 200, "should return OK code")
        self.assertEqual(updated_user, user, "should return the replaced user")
        self.assertIn(updated_user, self.endpoints.repository.users, "replaced user should be in repository")

    def test_delete_user(self):
        user_id_to_delete = 2
        response, status = self.endpoints.delete_user(user_id_to_delete)
        self.assertEqual(status, 200, "should return OK code")
        self.assertEqual(response, {"message": "User deleted successfully"}, "should return successful deletion message")
        self.assertNotIn(user_id_to_delete, [u.user_id for u in self.endpoints.repository.users], "user should be removed from repository")

            
if __name__ == "__main__":
    unittest.main()
