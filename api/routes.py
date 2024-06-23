from flask import Blueprint
from api.user_api import get_users, get_user, create_user, update_user, delete_user

user_bp = Blueprint('user', __name__)

user_bp.route('/api/users', methods=['GET'])(get_users)
user_bp.route('/api/users/<int:user_id>', methods=['GET'])(get_user)
user_bp.route('/api/users', methods=['POST'])(create_user)
user_bp.route('/api/users/<int:user_id>', methods=['PUT'])(update_user)
user_bp.route('/api/users/<int:user_id>', methods=['DELETE'])(delete_user)
