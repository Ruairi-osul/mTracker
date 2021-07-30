from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms.fields import SubmitField
from wtforms.validators import DataRequired, Optional
from wtforms_sqlalchemy.fields import QuerySelectField
from mtracker.query_factories import (
    mouse_factory,
    data_type_factory,
    session_type_factory,
)
from mtracker.utils import get_pk


class AddDataSetForm(FlaskForm):
    mouse = QuerySelectField(
        "Mouse",
        validators=[DataRequired()],
        query_factory=mouse_factory,
        get_pk=get_pk,
        get_label="mouse_name",
    )
    data_type = QuerySelectField(
        "Data Type",
        validators=[DataRequired()],
        query_factory=data_type_factory,
        get_pk=get_pk,
        get_label="data_name",
    )
    session = QuerySelectField(
        label="Session (leave black if not session-sepecific)",
        validators=[Optional()],
        query_factory=session_type_factory,
        get_pk=get_pk,
        get_label="session_name",
        allow_blank=True
    )
    datafile = FileField(label="Datafile", validators=[DataRequired()])
    submit = SubmitField("Upload")
