from flask_wtf import FlaskForm
from wtforms import FileField, FloatField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileRequired

class RotateImageForm(FlaskForm):
    image = FileField('Upload Image', validators=[FileRequired()])
    angle = FloatField('Angle', validators=[DataRequired()])
    submit = SubmitField('Rotate Image')
