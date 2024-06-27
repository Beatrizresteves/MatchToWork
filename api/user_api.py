from flask import request, jsonify
from db import get_db_connection
from models.user import User


def user_to_json(user):
    return {
        'user_id': user.user_id,
        'username': user.username,
        'email': user.email,
        'fullname': user.fullname,
        'cpf': user.cpf,
        'phone_number': user.phone_number,
        'address_id': user.address_id,
        'registration_date': user.registration_date,
        'is_active': user.is_active,
    }


def get_users():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * from users')
    rows = cur.fetchall()
    users = [User.from_db_row(row) for row in rows]
    conn.close()
    return jsonify([user_to_json(user) for user in users]), 200


def get_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * from users WHERE user_id = %s', (user_id))
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
        user_id=None,  # Não passe 'user_id' ao criar um novo usuário
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


def update_user(user_id):
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        UPDATE users
        SET username = %s, email = %s, password = %s, fullname = %s, cpf = %s,
            phone_number = %s, address_id = %s, is_active = %s
        WHERE user_id = %s
    ''', (data['username'], data['email'], data['password'], data['fullname'], data['cpf'],
          data['phone_number'], data.get('address_id'), data.get('is_active', True), user_id))
    conn.commit()
    cur.execute('SELECT * FROM users WHERE user_id = %s', (user_id,))
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
