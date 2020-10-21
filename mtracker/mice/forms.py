from flask_wtf import FlaskForm
from wtforms.fields import (
    StringField,
    SubmitField,
    BooleanField,
)
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, ValidationError, Optional
from mtracker.models import Mouse
from wtforms_sqlalchemy.fields import QuerySelectField
from mtracker.query_factories import group_factory
from mtracker.utils import get_pk


class AddMouseForm(FlaskForm):
    mouse_name = StringField("Mouse Name", validators=[DataRequired(), Length(max=150)])
    dob = DateField("Birth Date", validators=[Optional()])
    cull_date = DateField("Cull Date", validators=[Optional()])
    is_done = BooleanField("Preprocessing finished", default=False)
    is_male = BooleanField("Is male", default=True)
    group = QuerySelectField(
        "Group",
        validators=[DataRequired()],
        query_factory=group_factory,
        get_label="group_name",
        get_pk=get_pk,
    )
    submit = SubmitField("Add Mouse")

    def validate_exp_name(self, exp_name):
        name_exists = Mouse.query.filter_by(exp_name=exp_name.data).first()
        if name_exists:
            raise ValidationError("An experiment with that name already exists.")


class UpdateMouseForm(FlaskForm):
    mouse_name = StringField("Mouse Name", validators=[DataRequired(), Length(max=150)])
    dob = DateField("Birth Date")
    cull_date = DateField("Cull Date")
    is_done = BooleanField("Preprocessing finished", default=False)
    group = QuerySelectField(
        "Group",
        validators=[DataRequired()],
        query_factory=group_factory,
        get_label="group_name",
        get_pk=get_pk,
    )
    submit = SubmitField("Update Mouse")
