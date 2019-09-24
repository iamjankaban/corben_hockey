from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LigaForm(FlaskForm):
    input_liga = StringField('input_liga', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class TeamsForm(FlaskForm):
    team_left  = StringField('team_left', validators=[DataRequired()])
    team_right = StringField('team_right', validators=[DataRequired()])
    submit = SubmitField('Sign In')