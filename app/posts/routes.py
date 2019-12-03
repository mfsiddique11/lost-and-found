from flask import request,jsonify,Blueprint,url_for
from app import app,db
from app.models import Post
from app.models import Category
from flask_login import current_user,login_required
import secrets
import os
from datetime import datetime
posts=Blueprint('posts','__name__')

                   

@posts.route('/post/create', methods=['POST'])
@login_required
def add_post():
        
        if Category.query.all() == []:
                return 'please add categories first'
        else:
                
                if 'description' not in request.form:
                        return 'description missing'
                if 'category' not in request.form:
                        return 'category missing'
                if 'itemName' not in request.form:
                        return 'itemName missing'
                if 'location' not in request.form:
                        return 'location missing'
                if 'image' not in request.files:
                        return 'image missing'                        
                pic=request.files['image']
                _,f_ext=os.path.splitext(pic.filename)
                random_hex=secrets.token_hex(4)
                picture_fn=_+random_hex+f_ext

                picture_path=os.path.join(app.root_path,'static/pictures',picture_fn)
                pic.save(picture_path)
                itemName=request.form['itemName']
                location=request.form['location']
                print(picture_path)
                
                category=Category.query.get(int(request.form['category']))
                description=request.form['description']

                new_post=Post(itemName=itemName,location=location,description=description,pic=picture_path,poster=current_user,postcategory=category)

                db.session.add(new_post)
                db.session.commit()

                return 'post created'






@posts.route('/post/<int:post_id>')
@login_required 
def get_post(post_id):
        post=Post.query.get_or_404(post_id)
        return post.itemName +'  ' + post.postcategory.name

@posts.route('/home')
@login_required 
def get_posts():
        post=current_user.posts.all()
        return "success"       


@posts.route('/post/<int:post_id>/update',methods=['PUT'])
@login_required 
def update_post(post_id):
        post=Post.query.get_or_404(post_id)
        if post.poster==current_user:
                if 'description' in request.form:
                        post.description=request.form['description']
                if 'category' in request.form:
                        post.postcategory=Category.query.get(int(request.form['category']))
                if 'itemName' in request.form:
                        post.itemName=request.form['itemName']
                if 'location' in request.form:
                        post.location=request.form['location'] 
                if 'image' in request.files:
                        pic=request.files['image'] 
                        _,f_ext=os.path.splitext(pic.filename)
                        random_hex=secrets.token_hex(4)
                        picture_fn=_+random_hex+f_ext
                        
                        os.remove(os.path.join(app.root_path,'static/pictures',post.pic))

                        picture_path=os.path.join(app.root_path,'static/pictures',picture_fn)
                        pic.save(picture_path)
                        post.pic=picture_fn


                
                db.session.commit()
                return 'successully updated'
        else:
                return 'you didnt post this post'        
        

@posts.route('/post/<int:post_id>/delete',methods=['DELETE'])
@login_required 
def delete_post(post_id):
        post=Post.query.get_or_404(post_id)
        if post.poster==current_user:
                os.remove(os.path.join(app.root_path,'static/pictures',post.pic))
                
                
                db.session.delete(post)
                db.session.commit()
                return "deleted" 
        else:
                return 'you didnt post this post'
             
@posts.route('/post/search')
@login_required 
def search_post():
        if 'itemname' in request.args and 'location' in request.args:
                posts=Post.query.filter_by(itemName=request.args.get('itemname'),location=request.args.get('location')).all()
                print(posts)
                return 'success'
        elif 'itemname' in request.args: 
                posts=Post.query.filter_by(itemName=request.args.get('itemname')).all()
                print(posts)
                return 'success' 
        elif 'location' in request.args:
                posts=Post.query.filter_by(location=request.args.get('location')).all()
                print(posts)
                return 'success'      
        else:
                return 'add query to the search'
                
