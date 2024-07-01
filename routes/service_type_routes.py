from flask import Blueprint
from api.service_type_api import get_services_types, get_service_type, create_service_type, patch_service_type, put_service_type, delete_service_type

service_type_bp = Blueprint('service_type_api', __name__)

service_type_bp.add_url_rule('/servicetypes', 'get_servicetypes',
                             get_services_types, methods=['GET'])
service_type_bp.add_url_rule('/servicetypes/<int:service_type_id>',
                             'get_service_type', get_service_type, methods=['GET'])
service_type_bp.add_url_rule('/servicetypes', 'create_service_type',
                             create_service_type, methods=['POST'])
service_type_bp.add_url_rule('/servicetypes/<int:service_type_id>',
                             'put_service_type', put_service_type, methods=['PUT'])
service_type_bp.add_url_rule('/servicetypes/<int:service_type_id>',
                             'patch_service_type', patch_service_type, methods=['PATCH'])
service_type_bp.add_url_rule('/servicetypes/<int:service_type_id>',
                             'delete_service_type', delete_service_type, methods=['DELETE'])
