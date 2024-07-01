from flask import Blueprint
from api.user_api import get_users, get_user, create_user, patch_user, put_user, delete_user

user_bp = Blueprint('user', __name__)

user_bp.route('/users', methods=['GET'])(get_users)
user_bp.route('/users/<int:user_id>', methods=['GET'])(get_user)
user_bp.route('/users', methods=['POST'])(create_user)
user_bp.route('/users/<int:user_id>', methods=['PUT'])(put_user)
user_bp.route('/users/<int:user_id>', methods=['PATCH'])(patch_user)
user_bp.route('/users/<int:user_id>', methods=['DELETE'])(delete_user)
