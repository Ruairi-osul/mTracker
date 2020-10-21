from flask import Blueprint, url_for, redirect, render_template, flash, request
from sqlalchemy.exc import IntegrityError
from mtracker.models import SurgeryType
from mtracker.extentions import db
from mtracker.surgery_types.forms import AddSurgeryTypeForm, UpdateSurgeryTypeForm


surgery_types = Blueprint("surgery_types", __name__)


@surgery_types.route("/view_surgery_types", methods=["GET", "POST"])
def view_surgery_types():
    page = request.args.get("page", 1, type=int)
    surgery_types = SurgeryType.query.paginate(per_page=20, page=page)
    return render_template(
        "surgery_types/view_surgery_types.html", page=page, surgery_types=surgery_types
    )


@surgery_types.route("/surgery_type/add", methods=["GET", "POST"])
def add_surgery_type():
    form = AddSurgeryTypeForm()
    if form.validate_on_submit():
        new_surgery_type = SurgeryType(
            surgery_name=form.surgery_name.data,
            surgery_description=form.surgery_description.data,
        )
        db.session.add(new_surgery_type)
        db.session.commit()
        flash(
            f"SurgeryType '{new_surgery_type.surgery_name}' added.", category="success"
        )
        return redirect(url_for("surgery_types.view_surgery_types"))
    return render_template("surgery_types/add_surgery_type.html", form=form)


@surgery_types.route("/surgery_type/<int:id>", methods=["GET", "POST"])
def single_surgery_type(id):
    surgery_type = SurgeryType.query.get_or_404(int(id))
    return render_template("surgery_types/surgery_type.html", surgery_type=surgery_type)


@surgery_types.route("/surgery_type/<int:id>/update", methods=["GET", "POST"])
def update_surgery_type(id):
    surgery_type = SurgeryType.query.get_or_404(int(id))
    form = UpdateSurgeryTypeForm()
    if request.method == "GET":
        form.surgery_name.data = surgery_type.surgery_name
        form.surgery_description.data = surgery_type.surgery_description
    if form.validate_on_submit():
        surgery_type.surgery_name = form.surgery_name.data
        surgery_type.surgery_description = form.surgery_description.data
        try:
            db.session.add(surgery_type)
            db.session.commit()
        except IntegrityError:
            flash(
                f"A session type with name '{surgery_type.surgery_name}' already exists.",
                category="danger",
            )
            db.session.rollback()
            return redirect(url_for("update_surgery_type"), id=id)
        flash(
            f"Sucesfully updataed surgery_type '{surgery_type.surgery_name}'",
            category="success",
        )
        return redirect(url_for("surgery_types.view_surgery_types"))
    return render_template("surgery_types/update_surgery_type.html", form=form)


@surgery_types.route("/surgery_type/<int:id>/delete", methods=["GET", "POST"])
def delete_surgery_type(id):
    surgery_type = SurgeryType.query.get_or_404(int(id))
    db.session.delete(surgery_type)
    db.session.commit()
    flash("Session type deleted", category="success")
    return redirect(url_for("surgery_types.view_surgery_types"))
