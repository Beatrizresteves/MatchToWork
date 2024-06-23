from flask import request, jsonify
from db import get_db_connection
from models.service import Service


def service_to_json(service):
    return {
        'service_id': service.service_id,
        'service_type_id': service.service_type_id,
        'client_id': service.client_id,
        'start_date': service.start_date,
        'end_date': service.end_date,
        'status': service. status,
    }


def get_services():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM services')
    rows = cur.fetchall()
    services = [Service.from_db_row(row) for row in rows]
    conn.close()
    return jsonify([service_to_json(service) for service in services]), 200


def get_service(service_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM services WHERE service_id = %s', (service_id,))
    row = cur.fetchone()
    conn.close()
    if row:
        service = Service.from_db_row(row)
        return jsonify(service_to_json(service)), 200
    else:
        return jsonify({'error': 'Service not found'}), 404


def create_service():
    data = request.get_json()
    new_service = Service(
        None,
        data['service_type_id'],
        data['client_id'],
        data['start_date'],
        data['end_date'],
        data['status']
    )
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO services (service_type_id, client_id, start_date, end_date, status)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING service_id
    ''', (new_service.service_type_id, new_service.client_id, new_service.start_date,
          new_service.end_date, new_service.status))
    new_service.service_id = cur.fetchone()[0]
    conn.commit()
    conn.close()
    return jsonify(service_to_json(new_service)), 201


def update_service(service_id):
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        UPDATE services
        SET service_type_id = %s, client_id = %s, start_date = %s, end_date = %s, status = %s
        WHERE service_id = %s
    ''', (data['service_type_id'], data['client_id'], data['start_date'], data['end_date'],
          data['status'], service_id))
    conn.commit()
    cur.execute('SELECT * FROM services WHERE service_id = %s', (service_id,))
    updated_service = Service.from_db_row(cur.fetchone())
    conn.close()
    return jsonify(service_to_json(updated_service)), 200


def delete_service(service_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM services WHERE service_id = %s', (service_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Service deleted'}), 200
