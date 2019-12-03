from flask import request,jsonify,Blueprint
from app import app,db
from app.models import Category

categories=Blueprint('categories','__name__')


@categories.route('/')
def check():
        return 'working'

@categories.route('/category/add',methods=['POST'])
def add_category():
        name=request.json['name']
        category=Category.query.filter_by(name=name).first()
        if category:
                return 'category already exists'
        else:
                new_category=Category(name=name)
                db.session.add(new_category)
                db.session.commit()
                return 'added category successfully'

@categories.route('/category/show',methods=['POST'])
def show_category():
        print(Category.query.all())
        return 'success'

@categories.route('/category/<int:category_id>')
def get_category(category_id):
        category=Category.query.get_or_404(category_id)
        return category.name

@categories.route('/category/<int:category_id>/update',methods=['PUT'])
def update_category(category_id):
        category=Category.query.get_or_404(category_id)
        category.name=request.json['name']
        db.session.commit()
        return 'updated succesfuly'

@categories.route('/category/<int:category_id>/delete',methods=['DELETE'])
def delete_category(category_id):
        category=Category.query.get_or_404(category_id)
        db.session.delete(category)
        db.session.commit()
        return "deleted" 
