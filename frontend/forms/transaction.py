from flask_wtf import FlaskForm
from wtforms import (
    FloatField,
    StringField,
    SubmitField
)
from wtforms.validators import (
    DataRequired,
    EqualTo,
    Length,
)



class TransactionForm(FlaskForm):
    amount = FloatField(validators=[DataRequired()])
    category = StringField(validators=[DataRequired(), Length(max=20)])
    submit = SubmitField("Submit")