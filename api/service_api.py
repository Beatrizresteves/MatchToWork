from flask import Flask, request, jsonify
from db import get_db_connection
from models.service import Service
from datetime import datetime
from logger_config import configure_logger
import psycopg2


app = Flask(__name__)
logger = configure_logger()

def service_to_json(service):
    return {
        'service_id': service.service_id,
        'service_type_id': service.service_type_id,
        'client_id': service.client_id,
        'start_date': service.start_date,
        'end_date': service.end_date,
        'status': service. status,
        'updated_at': service.updated_at,
        'created_at': service.created_at,
        'is_active': service.is_active,
    }
    
def log_and_return_error(message, status_code, service_id=None):
    log_info = {
        'request': f"{request.method} {request.path}",
        'status': status_code,
        'service_id': service_id,
        
    }
    logger.error(message, extra=log_info)
    return jsonify({'error': message}), status_code

def get_services():
    limit = request.args.get('limit', default=10, type=int)
    offset = request.args.get('offset', default=0, type=int)
    max_limit = 50
    if limit > max_limit:
        limit = 50
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('SELECT service_id, service_type_id, client_id, start_date, end_date, status FROM services LIMIT %s OFFSET %s', (limit, offset))
        rows = cur.fetchall()
        services = [Service.from_db_row(row) for row in rows]
        conn.close()
        logger.debug(f"Fetched {len(services)} services.", extra={
            'request': f"{request.method} {request.path}",
            'status': 200,
        })
        return jsonify([service_to_json(service) for service in services]), 200
    except Exception as e:
        conn.close()
        return log_and_return_error(f"Failed to fetch services: {str(e)}", 500)

def get_service(service_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('SELECT service_id, service_type_id, client_id, start_date, end_date, status FROM services WHERE service_id = %s', (service_id,))
        row = cur.fetchone()
        conn.close()
        if row:
            service = Service.from_db_row(row)
            logger.info(f"Fetched to service.", extra={
                'request': f"{request.method} {request.path}",
                'status': 200,
                'user_id': service_id,
            })
            return jsonify(service_to_json(service)), 200
        else:
            return log_and_return_error(f"Service not found", 404, service_id=service_id)
    except Exception as e:
        conn.close()
        return log_and_return_error(f"Failed to fetch service: {str(e)}", 500, service_id=service_id)

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
    try:
        cur.execute('''
            INSERT INTO services (service_type_id, client_id, start_date, end_date, status)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING service_id
        ''', (new_service.service_type_id, new_service.client_id, new_service.start_date,
            new_service.end_date, new_service.status))
        new_service.service_id = cur.fetchone()[0]
        conn.commit()
        conn.close()
        logger.debug(f"Created new service.", extra={
            'request': f"{request.method} {request.path}",
            'status': 201,
            'service_id': new_service.service_id,
        })
        return jsonify(service_to_json(new_service)), 201
    except Exception as e:
        conn.rollback()
        conn.close()
        return log_and_return_error(f"Failed to create service {str(e)}", 500)

def put_service(service_id):
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('''
            UPDATE services
            SET service_type_id = %s, client_id = %s, start_date = %s, end_date = %s, status = %s
            WHERE service_id = %s
        ''', (data['service_type_id'], data['client_id'], data['start_date'], data['end_date'],
            data['status'], service_id))
        conn.commit()
        cur.execute('SELECT service_id, service_type_id, client_id, start_date, end_date, status FROM services WHERE service_id = %s', (service_id,))
        updated_service = Service.from_db_row(cur.fetchone())
        conn.close()
        logger.debug(f"Update service.",   extra={
            'request': f"{request.method} {request.path}",
            'status': 200,
            'service_id': service_id,
        })
        return jsonify(service_to_json(updated_service)), 200
    except Exception as e:
        conn.rollback()
        conn.close()
        return log_and_return_error(f"Failed update service: {str(e)}", 500, service_id=service_id)
    
def patch_service(service_id):
    data = request.get_json()
    allowed_fields = ['service_type_id', 'client_id', 'start_date', 'end_date', 'status']
    
    set_statements = []
    values = []

    for field in allowed_fields:
        if field in data:
            set_statements.append(f"{field} = %s")
            values.append(data[field])

    
    if not set_statements:
        return jsonify({'error': 'No fields to update'}), 400

    update_query = f'''
        UPDATE services
        SET {', '.join(set_statements)}
        WHERE service_id = %s
    '''
    values.append(service_id)
    
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(update_query, tuple(values))
        conn.commit()
        cur.execute('SELECT service_id, service_type_id, client_id, start_date, end_date, status, updated_at FROM services WHERE service_id = %s', (service_id,))
        updated_service = Service.from_db_row(cur.fetchone())
        conn.close()
        logger.debug(f"Update service.",   extra={
            'request': f"{request.method} {request.path}",
            'status': 200,
            'service_id': service_id,
        })
        return jsonify(service_to_json(updated_service)), 200
    except Exception as e:
        conn.rollback()
        conn.close()
        return log_and_return_error(f"Failed patch service: {str(e)}", 500, service_id=service_id)
    
def delete_service(service_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('DELETE FROM services WHERE service_id = %s', (service_id))
        conn.commit()
        conn.close()
        logger.debug(f"Delete service.",   extra={
            'request': f"{request.method} {request.path}",
            'status': 200,
            'service_id': service_id,
        })
        return jsonify({'message': 'Service deleted'}), 200
    except Exception as e:
        conn.rollback()
        conn.close()
        return log_and_return_error(f"Failed to delete service: {str(e)}", 500, service_id=service_id)
    
if __name__ == '__main__':
    app.run(debug=True)