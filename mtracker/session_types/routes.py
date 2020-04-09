from flask import Blueprint, url_for, redirect, render_template, flash, request
from sqlalchemy.exc import IntegrityError
from mtracker.models import SessionType
from mtracker.extentions import db
from mtracker.session_types.forms import AddSessionTypeForm, UpdateSessionTypeForm


session_types = Blueprint("session_types", __name__)


@session_types.route("/view_session_types", methods=["GET", "POST"])
def view_session_types():
    page = request.args.get("page", 1, type=int)
    session_types = SessionType.query.paginate(per_page=20, page=page)
    return render_template(
        "session_types/view_session_types.html", page=page, session_types=session_types
    )


@session_types.route("/session_type/add", methods=["GET", "POST"])
def add_session_type():
    form = AddSessionTypeForm()
    if form.validate_on_submit():
        new_session_type = SessionType(
            session_name=form.session_name.data,
            session_description=form.session_description.data,
        )
        db.session.add(new_session_type)
        db.session.commit()
        flash(
            f"SessionType '{new_session_type.session_name}' added.", category="success"
        )
        return redirect(url_for("session_types.view_session_types"))
    return render_template("session_types/add_session_type.html", form=form)


@session_types.route("/session_type/<int:id>", methods=["GET", "POST"])
def single_session_type(id):
    session_type = SessionType.query.get_or_404(int(id))
    return render_template("session_types/session_type.html", session_type=session_type)


@session_types.route("/session_type/<int:id>/update", methods=["GET", "POST"])
def update_session_type(id):
    session_type = SessionType.query.get_or_404(int(id))
    form = UpdateSessionTypeForm()
    if request.method == "GET":
        form.session_name.data = session_type.session_name
        form.session_description.data = session_type.session_description
    if form.validate_on_submit():
        session_type.session_name = form.session_name.data
        session_type.session_description = form.session_description.data
        try:
            db.session.add(session_type)
            db.session.commit()
        except IntegrityError:
            flash(
                f"A session type with name '{session_type.session_name}' already exists.",
                category="danger",
            )
            db.session.rollback()
            return redirect(url_for("update_session_type"), id=id)
        flash(
            f"Sucesfully updataed session_type '{session_type.session_name}'",
            category="success",
        )
        return redirect(url_for("session_types.view_session_types"))
    return render_template("session_types/update_session_type.html", form=form)


@session_types.route("/session_type/<int:id>/delete", methods=["GET", "POST"])
def delete_session_type(id):
    session_type = SessionType.query.get_or_404(int(id))
    db.session.delete(session_type)
    db.session.commit()
    flash("Session type deleted", category="success")
    return redirect(url_for("session_types.view_session_types"))
