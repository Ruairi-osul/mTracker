from flask_wtf import FlaskForm
from wtforms.fields import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from mtracker.models import DataType


class AddDataTypeForm(FlaskForm):
    data_name = StringField(
        "Data Type Name", validators=[DataRequired(), Length(max=150)]
    )
    data_description = TextAreaField(
        label="Data Type Description", validators=[DataRequired()]
    )
    submit = SubmitField("Add Data Type Type")

    def validate_exp_name(self, exp_name):
        name_exists = DataType.query.filter_by(exp_name=exp_name.data).first()
        if name_exists:
            raise ValidationError("An experiment with that name already exists.")


class UpdateDataTypeForm(FlaskForm):
    data_name = StringField(
        "Data Type Name", validators=[DataRequired(), Length(max=150)]
    )
    data_description = TextAreaField(
        label="Data Type Description", validators=[DataRequired()]
    )
    submit = SubmitField("Update Data Type Type")
