from datetime import datetime
from psycopg2.extras import DateTimeTZRange


class User:
    def __init__(self, user_id, username, email, password, fullname, cpf, phone_number,
                 address_id=None, created_at=None, updated_at=None, is_active=True):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password = password
        self.fullname = fullname
        self.cpf = cpf
        self.phone_number = phone_number
        self.address_id = address_id
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
        self.is_active = is_active

    @classmethod
    def from_db_row(cls, row):
        user_id, username, email, password, fullname, cpf, phone_number, address_id, created_at, updated_at, is_active = row
        return cls(user_id, username, email, password, fullname, cpf, phone_number, address_id, created_at, updated_at, is_active)
