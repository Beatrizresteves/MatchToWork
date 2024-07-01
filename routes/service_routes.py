from flask import Blueprint
from api.service_api import get_services, get_service, create_service, patch_service, put_service, delete_service

service_bp = Blueprint('service_api', __name__)

service_bp.add_url_rule('/services', 'get_services',
                        get_services, methods=['GET'])
service_bp.add_url_rule('/services/<int:service_id>',
                        'get_service', get_service, methods=['GET'])
service_bp.add_url_rule('/services', 'create_service',
                        create_service, methods=['POST'])
service_bp.add_url_rule('/services/<int:service_id>',
                        'update_service', put_service, methods=['PUT'])
service_bp.add_url_rule('/services/<int:service_id>',
                        'update_service', patch_service, methods=['PATCH'])
service_bp.add_url_rule('/services/<int:service_id>',
                        'delete_service', delete_service, methods=['DELETE'])
