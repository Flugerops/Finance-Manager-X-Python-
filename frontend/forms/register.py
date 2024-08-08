from flask_wtf import FlaskForm
from wtforms import (
    EmailField,
    StringField,
    PasswordField,
    SubmitField,
)
from wtforms.validators import (
    DataRequired,
    EqualTo,
    Length,

)
from wtforms_validators import AlphaNumeric


class RegisterForm(FlaskForm):
    nickname = StringField(
        validators=[DataRequired(), Length(min=5), AlphaNumeric()])
    password = PasswordField(validators=[DataRequired(), Length(min=10)])
    password_confirm = PasswordField(
        validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")
