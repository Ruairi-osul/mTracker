from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields import StringField, SubmitField
from wtforms.validators import DataRequired, Length
from wtforms_sqlalchemy.fields import QuerySelectField
from mtracker.query_factories import mouse_factory
from mtracker.utils import get_pk


class AddImageForm(FlaskForm):
    image_name = StringField("Image Name", validators=[DataRequired(), Length(max=150)])
    image_file = FileField(
        "Image File", validators=[FileAllowed(["tiff", "tif", "jpg", "png"])]
    )
    mouse = QuerySelectField(
        "Mouse", query_factory=mouse_factory, get_pk=get_pk, get_label="mouse_name"
    )
    submit = SubmitField("Add Image")
