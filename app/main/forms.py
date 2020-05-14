from flask_wtf import FlaskForm
from wtforms import TextAreaField,StringField,BooleanField,PasswordField,SubmitField,ValidationError,validators
from wtforms.validators import Required,Email,Length,EqualTo
from ..models import Users

class CommentForm(FlaskForm):
    review = TextAreaField('comment on the quote',validators=[Required()])
    submit = SubmitField('Submit')

class BlogForm(FlaskForm):

    title = StringField('Blog title',validators=[Required()])
    blogpost= TextAreaField('Write your blog post',validators=[Required()])
    submit = SubmitField('Submit')

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')

class SubscriptionForm(FlaskForm):
    email = StringField('Your Email Address',validators=[Required(),Email()])
    # email = StringField('Your Email Address', [validators.Length(min=6, max=35)])
    username = StringField('Enter your username',validators = [Required()])
    password = PasswordField('Password',validators = [Required(), EqualTo('password_confirm',message = 'Passwords must match')])
    password_confirm = PasswordField('Confirm Passwords',validators = [Required()])
    submit = SubmitField('Sign Up')
    

    def validate_email(self,data_field):
            if Users.query.filter_by(email =data_field.data).first():
                raise ValidationError('There is an account with that email')

    def validate_username(self,data_field):
        if Users.query.filter_by(username = data_field.data).first():
            raise ValidationError('That username is taken')