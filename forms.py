from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, EmailField, PasswordField, BooleanField

class AddUserForm(FlaskForm):
    """Form to sign up a user"""

    username = StringField("Username")
    
    password = PasswordField("Password")

    first_name = StringField("First Name")
    
    last_name = StringField("Last Name")
    
    email = EmailField("Email")

    
class LoginForm(FlaskForm):
    """Form for having the user login"""

    username = StringField("Username")
    
    password = PasswordField("Password")

class Add_New_Feedback(FlaskForm):
    """Form for having the user login"""

    title = StringField("Title")
    
    content = StringField("Content")

class Edit_Feedback(FlaskForm):
    """Form for having the user login"""

    title = StringField("Edit Title")
    
    content = StringField("Edit Content")

class Delete(FlaskForm):

    delete_post = BooleanField('Are you sure you want to delete? Check box for yes:')