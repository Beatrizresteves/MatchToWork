from flask import request, jsonify
from db import get_db_connection
from models.servicetype import ServiceType


def service_type_json(service_type):
    return {
        'service_type_id': service_type.service_type_id,
        'name': service_type.name,
        'description': service_type.description
    }


def get_services_types():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT service_type_id, name, description FROM servicetypes')
    rows = cur.fetchall()
    servicetypes = [ServiceType.from_db_row(row) for row in rows]
    conn.close()
    return jsonify([service_type_json(service_type) for service_type in servicetypes]), 200


def get_service_type(service_type_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT service_type_id, name, description FROM servicetypes FROM servicetypes WHERE service_type_id = %s',
                (service_type_id))
    row = cur.fetchone()
    conn.close()
    if row:
        service = ServiceType.from_db_row(row)
        return jsonify(service_type_json(service)), 200
    else:
        return jsonify({'error': 'ServiceType not found'}), 404


def create_service_type():
    data = request.get_json()
    new_service_type = ServiceType(
        None,
        data['name'],
        data['description']
    )
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
		INSERT INTO servicetypes (name, description)
        VALUES (%s, %s)
        RETURNING service_type_id
	''', (new_service_type.name, new_service_type.description))
    new_service_type.service_type_id = cur.fetchone()[0]
    conn.commit()
    conn.close()
    return jsonify(service_type_json(new_service_type)), 201


def update_service_type(service_type_id):
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
		UPDATE 	servicetypes
        SET name = %s, description = %s
        WHERE service_type_id = %s
	''', (data['name'], data['description']))
    conn.commit()
    cur.execute('SELECT service_type_id, name, description FROM servicetypes WHERE service_type_id = %s',
                (service_type_id,))
    update_service_type = ServiceType.from_db_row(cur.fetchone())
    conn.close()
    return jsonify(service_type_json(update_service_type)), 200


def delete_service_type(service_type_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        'DELETE FROM servicetypes WHERE service_type_id = %s', (service_type_id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'ServiceType deleted'}), 200
