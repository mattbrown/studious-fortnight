from flask import Blueprint, request, g, jsonify, make_response
from microblog.models import User
from microblog import db

bp = Blueprint('users', __name__, url_prefix='/users')


@bp.route('', methods=['GET'])
def get_users_endpoint():
    # Get users
    users = db.session.execute(db.select(User)).all()

    output = [u[0].to_dict() for u in users]
    return jsonify(output)


@bp.route('', methods=['POST'])
def post_users_endpoint():
    data = request.get_json()
    user = User(name=data['name'], email=data['email'])
    db.session.add(user)
    db.session.commit()

    return jsonify(user.to_dict())


@bp.route('/<uuid:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = db.get_or_404(User, user_id)
    return jsonify(user.to_dict())


@bp.route('/<uuid:user_id>', methods=['PUT'])
def update_user_by_id(user_id):
    user = db.get_or_404(User, user_id)
    data = request.get_json()
    user.name = data['name']
    user.email = data['email']

    db.session.add(user)
    db.session.commit()

    return jsonify(user.to_dict())


@bp.route('/<uuid:user_id>', methods=['DELETE'])
def delete_user_by_id(user_id):
    user = db.get_or_404(User, user_id)
    db.session.delete(user)
    db.session.commit()

    return make_response('', 204)
