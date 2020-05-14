from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin,AnonymousUserMixin
from . import login_manager
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Quote:
    '''
    Quote class to define quote objects
    '''
    def __init__(self,id,author,quote):
        self.id=id
        self.author=author
        self.quote=quote


class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),unique = True,index = True)
    role_id= db.Column(db.Integer,db.ForeignKey('roles.id'))
    pass_secure=db.Column(db.String(255))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    photos = db.relationship('PhotoProfile',backref = 'user',lazy = "dynamic")
    blogs = db.relationship('Blog',backref = 'userBlog',lazy = "dynamic")
    

    def can(self,permissions):
        return self.role is not None and \
            (self.role.permissions & permissions)==permissions
    
    def is_administator(self):
        return self.can(Permission.ADMINISTER)

    def __init__(self,**kwargs):
        super(User,self).__init__(**kwargs)
        if self.role is None:
            if self.email=='naikaesther5@gmail.com':
                self.role=Role.query.filter_by(permissions=0Xff).first()
            if self.role is None:
                self.role=Role.query.filter_by(default=True).first()
  

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')
    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)
    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)

    def save_user(self):
        db.session.add(self)
        db.session.commit()

class AnonymousUser(AnonymousUserMixin):
    def can(self,permissions):
        return False
    def is_administator(self):
        return False
    
class Comment(db.Model):

    __tablename__ = 'reviews'

    id = db.Column(db.Integer,primary_key = True)
    quote_id = db.Column(db.Integer,db.ForeignKey("blogposts.id")) 
    comment=db.Column(db.String)
    posted = db.Column(db.DateTime,default=datetime.utcnow)


    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comment(cls,id):
        reviews = Comment.query.filter_by(quote_id=id).all()
        return reviews


class Permission():
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255),unique=True)
    default=db.Column(db.Boolean, default=False, index=True)
    permissions=db.Column(db.Integer)
    users = db.relationship('User',backref = 'role',lazy="dynamic")
    
    

    def __repr__(self):
        return f'User {self.name}'

    def insert_roles():
        roles={
            'User':(Permission.COMMENT, True),
            'Moderator':(Permission.COMMENT |
            Permission.WRITE_ARTICLES|
            Permission.MODERATE_COMMENTS, False),
            'Administrator':(0xff, False)

        }
        for r in roles:
            role=Role.query.filter_by(name=r).first()
            if role is None:
                role=Role(name=r)
            role.permissions=roles[r][0]
            role.default=roles[r][1]
            db.session.add(role)
        db.session.commit()
class PhotoProfile(db.Model):
    __tablename__ = 'profile_photos'

    id = db.Column(db.Integer,primary_key = True)
    pic_path = db.Column(db.String())
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))

class Blog(db.Model):
    __tablename__ = 'blogposts'

    id = db.Column(db.Integer,primary_key = True)
    title= db.Column(db.String(255))
    quote = db.Column(db.String)
    posted = db.Column(db.DateTime,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    comments = db.relationship('Comment',backref = 'post',lazy="dynamic")
    def __str__(self):
        return self.title


    def save_blog(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_blog_title(cls,title):
        blog = Blog.query.filter_by(title=title).all()
        return blog
    
    @classmethod
    def get_blog(cls,id):
        blog = Blog.query.filter_by(id=id).first()
        return blog

    @classmethod
    def get_blogs(cls,id):
        blog = Blog.query.filter_by(id=id).all()
        return blog

class Users(UserMixin,db.Model):
    __tablename__ = 'subscribers'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),unique = True,index = True)
    pass_secure=db.Column(db.String(255))
    
    
    

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')
    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)
    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)

    def save_user(self):
        db.session.add(self)
        db.session.commit()