from flask_wtf import FlaskForm
from wtforms import *

class signUpValidator(FlaskForm):
    
    class Meta:
        csrf = False
    
    name = StringField("name", validators=[
        validators.DataRequired(message="this field should be entered."),
        validators.length(min=4, max=20)
    ])
    
    family = StringField("family", validators=[
        validators.Optional(),
        validators.length(min=4, max=20)
    ])
    
    username = StringField("username", 
                            filters=[
        lambda x: x.strip() if x else x
    ],
                            validators=[
        validators.DataRequired(message="this field should be entered."),
        validators.length(min=4, max=20),
        validators.Regexp('^[A-Za-z][A-Za-z0-9_.]*$', message="Username must only contain letters, numbers, dots, and underscores.")
    ])
    
    password = PasswordField("password", validators=[
        validators.DataRequired(message="password is needed."),
        validators.length(min=8, max=32, message="password must be between 8 to 32 numbers.")
    ])
    
    number = StringField("number", validators=[
        validators.DataRequired(),
        validators.length(min=11, max=11)
    ])
    
class signInValidator(FlaskForm):
    
    username = StringField("username",
                           filters=[
                               lambda x: x.strip() if x else x
    ],
                           validators=[
        validators.DataRequired(message="this field should be entered."),
        validators.length(min=4, max=20),
        validators.Regexp('^[A-Za-z][A-Za-z0-9_.]*$', message="Username must only contain letters, numbers, dots, and underscores.")
    ])
    
    password = PasswordField("password", validators=[
        validators.DataRequired(message="password is needed."),
        validators.length(min=8, max=32, message="password must be between 8 to 32 numbers.")
    ])