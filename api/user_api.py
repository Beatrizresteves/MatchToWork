from flask import Flask, request, jsonify
from db import get_db_connection
from models.user import User
from datetime import datetime
from logger_config import configure_logger
from repository.user_repository import IRepository
import psycopg2

app = Flask(__name__)
logger = configure_logger()

class Endpoints:
    def __init__(self, repository: IRepository):
        self.repository = repository

    def get_users(self, limit: int = 10, offset: int = 0):
        users = self.repository.get_users(limit, offset)
        status = 200
        return users, status
    
    def create_user(self,user: User):
        self.repository.add_user(user)
        return user, 201
    

def user_to_json(user):
    return {
        'user_id': user.user_id,
        'username': user.username,
        'email': user.email,
        'fullname': user.fullname,
        'cpf': user.cpf,
        'phone_number': user.phone_number,
        'address_id': user.address_id,
        'created_at': user.created_at,
        'updated_at': user.updated_at, 
        'is_active': user.is_active,
    }

def log_and_return_error(message, status_code, user_id=None):
    log_info = {
        'request': f"{request.method} {request.path}",
        'status': status_code,
        'user_id': user_id,
        
    }
    logger.error(message, extra=log_info)
    return jsonify({'error': message}), status_code

def get_users():
    limit = request.args.get('limit', default=10, type=int)
    offset = request.args.get('offset', default=0, type=int)
    max_limit = 50
    if limit > max_limit:
        limit = 50
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('SELECT user_id, username, email, fullname, cpf, phone_number, address_id, created_at, updated_at, is_active FROM users LIMIT %s OFFSET %s', (limit, offset))
        rows = cur.fetchall()
        users = [User.from_db_row(row) for row in rows]
        conn.close()
        logger.debug("Fetched users.", extra={
            'request': f"{request.method} {request.path}",
            'status': 200,
        })
        return jsonify([user_to_json(user) for user in users]), 200
    except Exception as e:
        conn.close()
        return log_and_return_error(f"Failed to fetch users: {str(e)}", 500)
    
def get_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('SELECT user_id, username, email, fullname, cpf, phone_number, address_id, created_at, updated_at, is_active FROM users WHERE user_id = %s', (user_id,))
        row = cur.fetchone()
        conn.close()
        if row:
            user = User.from_db_row(row)
            logger.debug("Fetched user.", extra={
                'request': f"{request.method} {request.path}",
                'status': 200,
                'user_id': user_id,
            })
            return jsonify(user_to_json(user)), 200
        else:
            return log_and_return_error(f"User not found", 404, user_id=user_id)
    except Exception as e:
        conn.close()
        return log_and_return_error(f"Failed to fetch user {str(e)}", 500, user_id=user_id)

def create_user():
    data = request.get_json()
    new_user = User(
        user_id=None,
        username=data['username'],
        email=data['email'],
        password=data['password'],
        fullname=data['fullname'],
        cpf=data['cpf'],
        phone_number=data['phone_number'],
        address_id=data.get('address_id'),
        is_active=data.get('is_active', True)
    )
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('''
            INSERT INTO users (username, email, password, fullname, cpf, phone_number, address_id, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING user_id
        ''', (new_user.username, new_user.email, new_user.password, new_user.fullname, new_user.cpf,
              new_user.phone_number, new_user.address_id, new_user.is_active))
        new_user_id = cur.fetchone()[0]
        conn.commit()
        conn.close()
        new_user.user_id = new_user_id
        logger.debug("Created new user.", extra={
            'request': f"{request.method} {request.path}",
            'status': 201,
            'user_id': new_user_id,
        })
        return jsonify(user_to_json(new_user)), 201
    except psycopg2.IntegrityError as e:
        conn.rollback()
        conn.close()
        return jsonify({'error': 'Email already exists'}), 400
    except Exception as e:
        conn.rollback()
        conn.close()
        return log_and_return_error(f"Failed to create user: {str(e)}"), 500

def put_user(user_id):
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('''
            UPDATE users
            SET username = %s, email = %s, password = %s, fullname = %s, cpf = %s,
                phone_number = %s, address_id = %s, is_active = %s
            WHERE user_id = %s
        ''', (data['username'], data['email'], data['password'], data['fullname'], data['cpf'],
              data['phone_number'], data.get('address_id'), data.get('is_active', True), user_id))
        
        conn.commit()

        cur.execute('SELECT user_id, username, email, fullname, cpf, phone_number, address_id, created_at, updated_at, is_active FROM users WHERE user_id = %s', (user_id,))
        updated_user = User.from_db_row(cur.fetchone())

        conn.close()

        logger.debug("Updated user.", extra={
            'request': f"{request.method} {request.path}",
            'status': 200,
            'user_id': user_id,
        })
        return jsonify(user_to_json(updated_user)), 200
    except Exception as e:
        conn.rollback()
        conn.close()
        return log_and_return_error(f"Failed updated user. {str(e)}", 500, user_id=user_id)

def patch_user(user_id):
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        allowed_fields = ['username', 'email', 'password', 'fullname', 'cpf', 'phone_number', 'address_id', 'is_active']

        set_statements = []
        values = []

        for field in allowed_fields:
            if field in data:
                set_statements.append(f"{field} = %s")
                values.append(data[field])

        values.append(datetime.utcnow())
        values.append(user_id)

        cur.execute(f'''
            UPDATE users
            SET {', '.join(set_statements)}, updated_at = %s
            WHERE user_id = %s
        ''', tuple(values))

        conn.commit()

        cur.execute('SELECT user_id, username, email, fullname, cpf, phone_number, address_id, created_at, updated_at, is_active FROM users WHERE user_id = %s', (user_id,))
        updated_user = User.from_db_row(cur.fetchone())

        conn.close()
        logger.debug("Patch user.", extra={
            'request': f"{request.method} {request.path}",
            'status': 200,
            'user_id': user_id,
        })
        return jsonify(user_to_json(updated_user)), 200
    except Exception as e:
        conn.rollback()
        conn.close()
        return log_and_return_error(f"Failed patched user: {str(e)}", 500, user_id=user_id)

def delete_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('DELETE FROM users WHERE user_id = %s', (user_id,))
        conn.commit()
        conn.close()
        logger.debug("Delete user.", extra={
            'request': f"{request.method} {request.path}",
            'status': 200,
            'user_id': user_id,
        })
        return jsonify({'message': 'User deleted'}), 200
    except Exception as e:
        conn.rollback()
        conn.close()
        return log_and_return_error(f"Failed to delete user: {str(e)}", 500, user_id=user_id)

if __name__ == '__main__':
    app.run(debug=True)
