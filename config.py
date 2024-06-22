import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'minha_chave_secreta'
    DB_NAME = 'match_to_work_db'
    DB_USER = 'work'
    DB_PASSWORD = 'work'
    DB_HOST = 'localhost'
    DB_PORT = '5432'
