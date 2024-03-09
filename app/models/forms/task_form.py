from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Length

class TaskForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired(), Length(max=200)])
    user_id = IntegerField('User ID', validators=[DataRequired()])