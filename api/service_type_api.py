from flask import Flask, request, jsonify
from db import get_db_connection
from models.servicetype import ServiceType
from logger_config import configure_logger

app = Flask(__name__)
logger = configure_logger()

def service_type_json(service_type):
    return {
        'service_type_id': service_type.service_type_id,
        'name': service_type.name,
        'description': service_type.description,
        'updated_at': service_type.updated_at,
        'is_active': service_type.is_active,
    }

def log_and_return_error(message, status_code):
    logger.error(message)
    return jsonify({'error': message}), status_code

def get_services_types():
    limit = request.args.get('limit', default=10, type=int)
    offset = request.args.get('offset', default=0, type=int)
    max_limit = 50
    if limit > max_limit:
        limit = 50
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('SELECT service_type_id, name, description FROM servicetypes LIMIT %s OFFSET %s', (limit, offset))
        rows = cur.fetchall()
        servicetypes = [ServiceType.from_db_row(row) for row in rows]
        conn.close()
        logger.info(f"Fetched {len(servicetypes)}servicetypes.")
        return jsonify([service_type_json(service_type) for service_type in servicetypes]), 200
    except Exception as e:
        conn.close()
        return log_and_return_error(f"Failed to fetch servicetypes: {str(e)}", 500)

def get_service_type(service_type_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('SELECT service_type_id, name, description FROM servicetypes FROM servicetypes WHERE service_type_id = %s',
                    (service_type_id))
        row = cur.fetchone()
        conn.close()
        if row:
            service = ServiceType.from_db_row(row)
            logger.info(f"Fetched service type {service_type_id}")
            return jsonify(service_type_json(service)), 200
        else:
            return log_and_return_error(f"Service type {service_type_id} not found", 404)
    except Exception as e:
        conn.close()
        log_and_return_error(f"Failed to fetch {service_type_id} service type: {str(e)}")


def create_service_type():
    data = request.get_json()
    new_service_type = ServiceType(
        None,
        data['name'],
        data['description']
    )
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('''
            INSERT INTO servicetypes (name, description)
            VALUES (%s, %s)
            RETURNING service_type_id
        ''', (new_service_type.name, new_service_type.description))
        new_service_type.service_type_id = cur.fetchone()[0]
        conn.commit()
        conn.close()
        logger.info(f"Created new service type: {new_service_type.service_type_id}")
        return jsonify(service_type_json(new_service_type)), 201
    except Exception as e:
        conn.rollback()
        conn.close()
        return log_and_return_error(f"Failed to create service type {str(e)}", 500)
    
def put_service_type(service_type_id):
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    try:
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
        logger.info(f"Updated service type {service_type_id}")
        return jsonify(service_type_json(update_service_type)), 200
    except Exception as e:
        conn.rollback()
        conn.close()
        return log_and_return_error(f"Failed updated user {service_type_id}: {str(e)}", 500)
    
def patch_service_type(service_type_id):
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        allowed_fields = ['name', 'description']
        set_statements = []
        values = []

        for field in allowed_fields:
            if field in data:
                set_statements.append(f"{field} = %s")
                values.append(data[field])

        if not set_statements:
            return jsonify({'error': 'No valid fields provided to update.'}), 400

        set_clause = ', '.join(set_statements)
        values.append(service_type_id)

        cur.execute(f'''
            UPDATE servicetypes
            SET {set_clause}
            WHERE service_type_id = %s
        ''', values)
        conn.commit()

        cur.execute('SELECT service_type_id, name, description FROM servicetypes WHERE service_type_id = %s',
                    (service_type_id,))
        updated_service_type = ServiceType.from_db_row(cur.fetchone())
        conn.close()
        logger.info(f"Patched service type: {service_type_id}")
        return jsonify(service_type_json(updated_service_type)), 200
    except Exception as e:
        conn.rollback()
        conn.close()
        return log_and_return_error(f"Failed patch service type {service_type_id}: {str(e)}", 500)
    
def delete_service_type(service_type_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            'DELETE FROM servicetypes WHERE service_type_id = %s', (service_type_id))
        conn.commit()
        conn.close()
        return jsonify({'message': 'ServiceType deleted'}), 200
    except Exception as e:
        conn.rollback()
        conn.close()
        return log_and_return_error(f"Failed to delete service type {service_type_id}: {str(e)}", 500)
    

if __name__ == '__main__':
    app.run(debug=True)