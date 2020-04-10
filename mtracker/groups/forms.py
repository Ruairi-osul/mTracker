from flask_wtf import FlaskForm
from wtforms.fields import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from wtforms_sqlalchemy.fields import QuerySelectField
from mtracker.models import Group, Experiment
from mtracker.utils import get_pk


def experiment_query_factory():
    return Experiment.query


class AddGroupForm(FlaskForm):
    group_name = StringField("Group Name", validators=[DataRequired(), Length(max=150)])
    group_description = TextAreaField(
        label="Group Description", validators=[DataRequired()]
    )
    experiment = QuerySelectField(
        label="Experiment",
        validators=[DataRequired()],
        query_factory=experiment_query_factory,
        allow_blank=False,
        get_label="exp_name",
        get_pk=get_pk,
    )
    genotype = StringField("Genotype", validators=[DataRequired(), Length(max=150)])
    submit = SubmitField("Add Group Type")

    def validate_exp_name(self, exp_name):
        name_exists = Group.query.filter_by(exp_name=exp_name.data).first()
        if name_exists:
            raise ValidationError("An experiment with that name already exists.")


class UpdateGroupForm(FlaskForm):
    group_name = StringField("Group Name", validators=[DataRequired(), Length(max=150)])
    group_description = TextAreaField(
        label="Group Description", validators=[DataRequired()]
    )
    experiment = QuerySelectField(
        label="Experiment",
        validators=[DataRequired()],
        query_factory=experiment_query_factory,
        allow_blank=False,
        get_label="experiment_name",
        get_pk=get_pk,
    )
    genotype = StringField("Genotype", validators=[DataRequired(), Length(max=150)])
    submit = SubmitField("Update Group Type")
