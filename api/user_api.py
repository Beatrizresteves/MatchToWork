from flask import request, jsonify
from db import get_db_connection
from models.user import User
from datetime import datetime


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
        'update_at': user.update_at,
        'is_active': user.is_active,
    }


def get_users():
    limit = request.args.get('limit', default=10, type=int)
    offset = request.args.get('offset', default=0, type=int)
    max_limit = 50
    if limit > max_limit:
        limit = 50
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT user_id, username, email, fullname, cpf, phone_number, address_id, created_at, update_at, is_active FROM users LIMIT %s OFFSET %s', (limit, offset))
    rows = cur.fetchall()
    users = [User.from_db_row(row) for row in rows]
    conn.close()
    return jsonify([user_to_json(user) for user in users]), 200


def get_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT user_id, username, email, fullname, cpf, phone_number, address_id, created_at, update_at, is_active FROM users WHERE user_id = %s', (user_id,))
    row = cur.fetchone()
    conn.close()
    if row:
        user = User.from_db_row(row)
        return jsonify(user_to_json(user)), 200
    else:
        return jsonify({'error': 'User not found'}), 404


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
    return jsonify(user_to_json(new_user)), 201


def put_user(user_id):
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('''
        UPDATE users
        SET username = %s, email = %s, password = %s, fullname = %s, cpf = %s,
            phone_number = %s, address_id = %s, is_active = %s
        WHERE user_id = %s
    ''', (data['username'], data['email'], data['password'], data['fullname'], data['cpf'],
          data['phone_number'], data.get('address_id'), data.get('is_active', True), datetime.utcnow(), user_id))
    
    conn.commit()

    cur.execute('SELECT user_id, username, email, fullname, cpf, phone_number, address_id, created_at, update_at, is_active FROM users WHERE user_id = %s', (user_id,))
    updated_user = User.from_db_row(cur.fetchone())

    conn.close()

    return jsonify(user_to_json(updated_user)), 200

def patch_user(user_id):
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()

    allowed_fields = ['username', 'email', 'password', 'fullname', 'cpf', 'phone_number', 'address_id', 'is_active']

    set_statements = []
    values = []

    for field in allowed_fields:
        if field in data:
            set_statements.append(f"{field} = %s")
            values.append(data[field])

    values.append(datetime.utcnow())

    values.append(user_id)

    cur.execute('''
        UPDATE users
        SET {}
        WHERE user_id = %s
    '''.format(', '.join(set_statements)), tuple(values))

    conn.commit()

    cur.execute('SELECT user_id, username, email, fullname, cpf, phone_number, address_id, created_at, update_at, is_active FROM users WHERE user_id = %s', (user_id,))
    updated_user = User.from_db_row(cur.fetchone())

    conn.close()

    return jsonify(user_to_json(updated_user)), 200

def delete_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM users WHERE user_id = %s', (user_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'User deleted'}), 200
