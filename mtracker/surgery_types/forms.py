from flask_wtf import FlaskForm
from wtforms.fields import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from mtracker.models import SurgeryType


class AddSurgeryTypeForm(FlaskForm):
    surgery_name = StringField(
        "Surgery Name", validators=[DataRequired(), Length(max=150)]
    )
    surgery_description = TextAreaField(
        label="Surgery Description", validators=[DataRequired()]
    )
    submit = SubmitField("Add")

    def validate_exp_name(self, exp_name):
        name_exists = SurgeryType.query.filter_by(exp_name=exp_name.data).first()
        if name_exists:
            raise ValidationError("A surgery with that name already exists.")


class UpdateSurgeryTypeForm(FlaskForm):
    surgery_name = StringField(
        "Surgery Name", validators=[DataRequired(), Length(max=150)]
    )
    surgery_description = TextAreaField(
        label="Surgery Description", validators=[DataRequired()]
    )
    submit = SubmitField("Update")
