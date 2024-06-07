from flask_wtf import FlaskForm
from wtforms import FileField, FloatField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from flask_wtf.file import FileRequired, FileAllowed

def image_file_check(form, field):
    if not field.data.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
        raise ValidationError('Invalid file type. Please upload an image file.')

class RotateImageForm(FlaskForm):
    image = FileField('Upload Image', validators=[FileRequired(), image_file_check])
    angle = FloatField('Angle', validators=[DataRequired()])
    submit = SubmitField('Rotate Image')
#
