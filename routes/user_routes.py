from flask import Blueprint
from api.user_api import get_users, get_user, create_user, update_patch_user, update_put_user, delete_user

user_bp = Blueprint('user', __name__)

user_bp.route('/users', methods=['GET'])(get_users)
user_bp.route('/users/<int:user_id>', methods=['GET'])(get_user)
user_bp.route('/users', methods=['POST'])(create_user)
user_bp.route('/users/<int:user_id>', methods=['PUT'])(update_put_user)
user_bp.route('/users/<int:user_id>', methods=['PATCH'])(update_patch_user)
user_bp.route('/users/<int:user_id>', methods=['DELETE'])(delete_user)
