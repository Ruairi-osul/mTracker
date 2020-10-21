from flask_wtf import FlaskForm
from wtforms.fields import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from mtracker.models import SessionType


class AddSessionTypeForm(FlaskForm):
    session_name = StringField(
        "Session Name", validators=[DataRequired(), Length(max=150)]
    )
    session_description = TextAreaField(
        label="Session Description", validators=[DataRequired()]
    )
    submit = SubmitField("Add Session Type")

    def validate_exp_name(self, exp_name):
        name_exists = SessionType.query.filter_by(exp_name=exp_name.data).first()
        if name_exists:
            raise ValidationError("An experiment with that name already exists.")


class UpdateSessionTypeForm(FlaskForm):
    session_name = StringField(
        "Session Name", validators=[DataRequired(), Length(max=150)]
    )
    session_description = TextAreaField(
        label="Session Description", validators=[DataRequired()]
    )
    submit = SubmitField("Update Session Type")
