from flask_wtf import FlaskForm
from wtforms.fields import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from mtracker.models import Experiment


class AddExperimentForm(FlaskForm):
    exp_name = StringField(
        "Experiment Name", validators=[DataRequired(), Length(max=150)]
    )
    exp_description = TextAreaField(
        label="Experiment Description", validators=[DataRequired()]
    )
    submit = SubmitField("Add Experiment")

    def validate_exp_name(self, exp_name):
        name_exists = Experiment.query.filter_by(exp_name=exp_name.data).first()
        if name_exists:
            raise ValidationError("An experiment with that name already exists.")


class UpdateExperimentForm(FlaskForm):
    exp_name = StringField(
        "Experiment Name", validators=[DataRequired(), Length(max=150)]
    )
    exp_description = TextAreaField(
        label="Experiment Description", validators=[DataRequired()]
    )
    submit = SubmitField("Update Experiment")
