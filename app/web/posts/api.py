import os
import secrets

from flask import request, jsonify, Blueprint
from flask_login import current_user, login_required

from app import app, db
from app.decorators.category_required import category_required

from app.common.decorators.validate_json import validate_json
from app.models.category_model import Category
from app.models.post_model import Post
from app.web.posts.schemas import update_post_schema, add_post_schema

posts = Blueprint('posts', '__name__')


@posts.route('/post', methods=['POST'])
@login_required
@category_required
@validate_json(add_post_schema)
def add_post():
    image = request.files['image']
    image_name, image_ext = os.path.splitext(image.filename)
    picture = image_name + secrets.token_hex(4) + image_ext

    image_path = os.path.join(app.root_path, 'static/pictures', picture)
    image.save(image_path)

    new_post = Post(itemName=request.form['itemName'],
                    location=request.form['location'],
                    description=request.form['description'],
                    pic=picture,
                    poster=current_user,
                    postcategory=Category.query.get(int(request.form['category'])))

    db.session.add(new_post)
    db.session.commit()
    return jsonify({"Action": 'post created'}), 201


@posts.route('/post/<int:post_id>')
@login_required
def get_post(post_id):
    post = Post.query.get(post_id)
    if post:
        return jsonify(post), 200
    return jsonify({"Error": 'No post found'}), 404


@posts.route('/post')
@login_required
def get_posts():
    post = current_user.posts.all()
    if post:
        return jsonify(post), 200
    return jsonify({"Error": 'No post found'}), 404


@posts.route('/post/<int:post_id>/', methods=['PUT'])
@login_required
@validate_json(update_post_schema)
def update_post(post_id):
    post = Post.query.get(post_id)

    if not post:
        return jsonify({"Error": 'No post found'}), 404

    if post.poster != current_user:
        return jsonify({"Error": 'No post found'}), 404

    if 'description' in request.form:
        post.description = request.form['description']
    if 'category' in request.form:
        post.postcategory = Category.query.get(int(request.form['category']))
    if 'itemName' in request.form:
        post.itemName = request.form['itemName']
    if 'location' in request.form:
        post.location = request.form['location']
    if 'image' in request.files:
        os.remove(os.path.join(app.root_path, 'static/pictures', post.pic))

        image = request.files['image']

        image_name, image_ext = os.path.splitext(image.filename)
        picture = image_name + secrets.token_hex(4) + image_ext

        image_path = os.path.join(app.root_path, 'static/pictures', picture)
        image.save(image_path)
        post.pic = picture
        db.session.commit()

    return jsonify({"Action": 'post updated'}), 201


@posts.route('/post/<int:post_id>/', methods=['DELETE'])
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)

    if not post:
        return jsonify({"Error": 'No post found'}), 404

    if post.poster != current_user:
        return jsonify({"Error": 'No post found'}), 404

    os.remove(os.path.join(app.root_path, 'static/pictures', post.pic))
    db.session.delete(post)
    db.session.commit()
    return jsonify({"Action": 'post deleted'}), 201


@posts.route('/post/search')
@login_required
def search_post():
    if 'itemname' in request.args and 'location' in request.args:
        post = Post.query.filter_by(itemName=request.args.get('itemname'), location=request.args.get('location')).all()
        return jsonify(post), 200

    elif 'itemname' in request.args:
        post = Post.query.filter_by(itemName=request.args.get('itemname')).all()
        return jsonify(post), 200

    elif 'location' in request.args:
        post = Post.query.filter_by(location=request.args.get('location')).all()
        return jsonify(post), 200

    else:
        return jsonify({"Error": 'No post found'}), 404
