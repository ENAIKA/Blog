from flask import render_template,request,abort,redirect,url_for,flash
from app.main import main
from flask_login import login_required, current_user
from ..requests import get_quote
from .forms import CommentForm,UpdateProfile, BlogForm, SubscriptionForm
from .. import db, photos
from ..models import Comment, User, Quote,Blog,Users,Permission
import markdown2
from sqlalchemy import desc
from ..email import mail_message
from app.decorators import admin_required, permission_required


@main.route('/')
def index():
    title="Welcome to Nakish blog site"
    quote=get_quote()
    return render_template('index.html',title = title, quote=quote)

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    

    return render_template("profile/profile.html", user = user)


@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        user.save_user()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form = form)

@main.route('/user/<uname>/update/pic',methods = ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
        # return filename
    return redirect(url_for('main.profile',uname=user.username))
@main.route('/blogpost/comment/new/<int:id>', methods = ['GET','POST'])
def new_comment(id):
    form = CommentForm()
    
    blog=Blog.get_blog(id)

    if form.validate_on_submit():
        print('form is valid')
        
        review = form.review.data

        # Updated comment instance
        # import pdb; pdb.set_trace()
        new_comment = Comment(quote_id=blog.id,comment=review)

        # save comment method
        new_comment.save_comment()
        return redirect(url_for('.comment',id = new_comment.quote_id ))
    print('form is not vaild')
    title = 'comment'
    return render_template('new_comment.html',title = title, comment_form=form, blog=blog)
@main.route('/comment/<int:id>')
def single_comment(id):
# put,post
# mode
    comments=Comment.query.get(id)
    print(comments)
    format_review = markdown2.markdown("",extras=["code-friendly", "fenced-code-blocks"])
    if comments is None:
        abort(404)
        format_review = markdown2.markdown(comments.comment,extras=["code-friendly", "fenced-code-blocks"])
    return render_template('comment.html',comments = comments,format_comment=format_review)

@main.route('/blogpost/new/', methods = ['GET','POST'])
@login_required
def newblog():
    
    form = BlogForm() 
    

    if form.validate_on_submit():
        title = form.title.data
        blogPost = form.blogpost.data

        # Updated Post instance
        new_post = Blog(quote=blogPost,title=title,userBlog=current_user)

        # save blog method
        new_post.save_blog()
        return redirect(url_for('.blog', title=title,id=new_post.id))

    title = 'BlogPost'
    return render_template('blog.html',title = title, blog_form=form)

@main.route('/blog/<int:id>')
def blog(id):

    '''
    View movie page function that returns the movie details page 
    '''
    blogPosted= Blog.get_blog(id)
    blog_id=blogPosted.id
    title = ' comments'
    blog = Comment.get_comment(blogPosted.id)
    

    return render_template('new_blog.html',title = title,blog = blogPosted,id=blog_id,comments=blog)
@main.route('/comments/<int:id>')
def comment(id):

    '''
    View movie page function that returns the movie details page 
    '''
    blog = Blog.get_blog(id)
    print(blog.title,blog.quote)
    title = "blog comments"
    reviews = Comment.get_comment(blog.id)
    print(Comment.query.filter_by(quote_id=id).first())
    return render_template('comment.html',title = title,blog=blog,id = blog.id,comments = reviews)

@main.route('/allblogs')
def allblogs():
    title = "blogs"
    blog=Blog.query.order_by(desc(Blog.posted)).all()
    return render_template('allblogs.html',title = title,blog=blog)


@main.route('/subscribe',methods = ["GET","POST"])
def subscribe():
    form = SubscriptionForm()
    if form.validate_on_submit():
        user = Users(email = form.email.data, username = form.username.data,password = form.password.data)
        db.session.add(user)
        db.session.commit()

        mail_message("Thank you for subscribing","email/subscribe_user",user.email,user=user)

        return redirect(url_for('.index'))
    title = "New Account"
    return render_template('email/subscribe.html',registration_form = form, title=title)

@main.route('/edit/<int:id>', methods=['GET','POST'])
@login_required
@permission_required(Permission.WRITE_ARTICLES)
def edit(id):
    
    blog=Blog.query.get(id)
    if current_user != blog.user_id:
        abort(403)

    form=BlogForm()
    if form.validate_on_submit():
        blog=form.blogpost.data
        db.session.add(blog)
        return redirect(url_for('.blog',id=id))
    form.blogpost.data=blog.quote
    return render_template('edit_blog.html', form=form)

@main.route('/delete/comment/<int:id>', methods=['PUT','GET','POST'])
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def delete(id):
    
    comments=Comment.get_comment(id)
    blog=Blog.get_blog(comments.quote_id)
    if current_user != blog.user_id:
        abort(403)
    comments=Comment.query.filter_by(id=comments.id).delete()
    db.session.commit()
    return redirect(url_for('edit_comment.html', id=blog.id))

@main.route('/delete/blog/<int:id>', methods=['GET','POST'])
@login_required
@permission_required(Permission.WRITE_ARTICLES)
def deleteblog(id):
    blogs=Blog.query.get(id)
    blog=Blog.get_blog(blogs.id)
    if current_user != blog.user_id:
        abort(403)

    blog=Blog.query.filter_by(id=id).delete()
    db.session.commit()
    flash('blog deleted successfully')
    return render_template('index.html')