from flask_wtf import FlaskForm
from wtforms.fields import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length

CATEGORY_CHOICES = [
    ("neurons", "Neurons"),
    ("neuronal_activity", "Neuronal Activity"),
    ("events", "Events"),
    ("continuous", "Continuous"),
]


class AddDataTypeForm(FlaskForm):
    data_name = StringField(
        "Data Type Name", validators=[DataRequired(), Length(max=150)]
    )
    data_description = TextAreaField(
        label="Data Type Description", validators=[DataRequired()]
    )
    category = SelectField("Category", choices=CATEGORY_CHOICES)
    submit = SubmitField("Add Data Type")


class UpdateDataTypeForm(FlaskForm):
    data_name = StringField(
        "Data Type Name", validators=[DataRequired(), Length(max=150)]
    )
    data_description = TextAreaField(
        label="Data Type Description", validators=[DataRequired()]
    )
    category = SelectField("Category", choices=CATEGORY_CHOICES)
    submit = SubmitField("Update Data Type")
