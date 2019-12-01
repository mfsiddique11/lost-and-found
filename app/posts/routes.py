from flask import request,jsonify,Blueprint
from app import app,db
from app.models import Post
from app.models import Category
from flask_login import current_user,login_required

posts=Blueprint('posts','__name__')



@posts.route('/post/create', methods=['POST'])
@login_required 
def add_post():
        # description=request.form['value'].description
        # print (description)
        # picture_file=save_picture(request.files['image'])
        if Category.query.all() == []:
                return 'please add categories first'
        else:
                description=request.json['description']
                pic=request.json['pic']
                itemName=request.json['itemName']
                location=request.json['location']
                category=Category.query.get(int(request.json['category']))

                new_post=Post(itemName=itemName,location=location,description=description,pic=pic,poster=current_user,postcategory=category)

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
        print (post)
        return "success"       


@posts.route('/post/<int:post_id>/update',methods=['POST'])
@login_required 
def update_post(post_id):
        post=Post.query.get_or_404(post_id)
        if post.poster==current_user:
                if 'description' in request.json:
                        post.description=request.json['description']
                if 'itemName' in request.json:
                        post.itemName=request.json['itemName']
                if 'pic' in request.json:
                        post.pic=request.json['pic']
                if 'location' in request.json:
                        post.location=request.json['location']        
                if 'category' in request.json: 
                        post.postcategory=Category.query.get(int(request.json['category']))
                db.session.commit()
                return 'successully updated'
        else:
                abort(403)        
        

@posts.route('/post/<int:post_id>/delete',methods=['POST'])
@login_required 
def delete_post(post_id):
        post=Post.query.get_or_404(post_id)
        if post.poster==current_user:
                
                db.session.delete(post)
                db.session.commit()
                return "deleted" 
        else:
                abort(403)
             
@posts.route('/post/search',methods=['GET'])
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
                