from flask import Blueprint, request, jsonify, make_response
from sqlalchemy.exc import IntegrityError

from microblog.models import User, Post
from microblog import db
import uuid


bp = Blueprint('posts', __name__, url_prefix='/posts')

@bp.route('', methods=['GET'])
def get_posts_endpoint():
    post_rows = db.session.execute(db.select(Post)).all()

    # Rows return as a tuple, so we need to fetch that out and get it ready for jsonifying
    output = [p[0].to_dict() for p in post_rows]
    return jsonify(output)

@bp.route('', methods=['POST'])
def post_posts_endpoint():
    data = request.get_json()
    post = Post(
        title= data['title'],
        content = data['content'],
        user_id = uuid.UUID(data['user_id'])
    )
    db.session.add(post)
    try:
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        if 'ForeignKeyViolation' in str(e):
            return 'User does not exist', 400
        else:
            return 'Something is wrong, please contact the admin', 500
    return jsonify(post.to_dict())

@bp.route('/<uuid:post_id>', methods=['GET'])
def get_post_endpoint(post_id):
    post = db.get_or_404(Post, post_id)
    return jsonify(post.to_dict())

@bp.route('/<uuid:post_id>', methods=['PUT'])
def update_post_endpoint(post_id):
    post = db.get_or_404(Post, post_id)
    data = request.get_json()
    post.title = data['title']
    post.content = data['content']
    post.user_id = data['user_id']

    db.session.add(post)
    try:
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        if 'ForeignKeyViolation' in str(e):
            return 'User does not exist', 400
        else:
            return 'Something is wrong, please contact the admin', 500

    return jsonify(post.to_dict())

@bp.route('/<uuid:post_id>', methods=['DELETE'])
def delete_post_endpoint(post_id):
    post = db.get_or_404(Post, post_id)
    db.session.delete(post)
    db.session.commit()

    return make_response('', 204)