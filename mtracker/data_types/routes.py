from flask import Blueprint, url_for, redirect, render_template, flash, request
from sqlalchemy.exc import IntegrityError
from mtracker.models import DataType
from mtracker.extentions import db
from mtracker.data_types.forms import AddDataTypeForm, UpdateDataTypeForm


data_types = Blueprint("data_types", __name__)


@data_types.route("/view_data_types", methods=["GET", "POST"])
def view_data_types():
    page = request.args.get("page", 1, type=int)
    data_types = DataType.query.paginate(per_page=20, page=page)
    return render_template(
        "data_types/view_data_types.html", page=page, data_types=data_types
    )


@data_types.route("/data_type/add", methods=["GET", "POST"])
def add_data_type():
    form = AddDataTypeForm()
    if form.validate_on_submit():
        new_data_type = DataType(
            data_name=form.data_name.data,
            data_description=form.data_description.data,
            category=form.category.data,
        )
        db.session.add(new_data_type)
        db.session.commit()
        flash(f"DataType '{new_data_type.data_name}' added.", category="success")
        return redirect(url_for("data_types.view_data_types"))
    return render_template("data_types/add_data_type.html", form=form)


@data_types.route("/data_type/<int:id>", methods=["GET", "POST"])
def single_data_type(id):
    data_type = DataType.query.get_or_404(int(id))
    return render_template("data_types/data_type.html", data_type=data_type)


@data_types.route("/data_type/<int:id>/update", methods=["GET", "POST"])
def update_data_type(id):
    data_type = DataType.query.get_or_404(int(id))
    form = UpdateDataTypeForm()
    if request.method == "GET":
        form.data_name.data = data_type.data_name
        form.data_description.data = data_type.data_description
        form.category.data = data_type.category.data
    if form.validate_on_submit():
        data_type.data_name = form.data_name.data
        data_type.data_description = form.data_description.data
        try:
            db.session.add(data_type)
            db.session.commit()
        except IntegrityError:
            flash(
                f"A session type with name '{data_type.data_name}' already exists.",
                category="danger",
            )
            db.session.rollback()
            return redirect(url_for("update_data_type"), id=id)
        flash(
            f"Sucesfully updataed data_type '{data_type.data_name}'",
            category="success",
        )
        return redirect(url_for("data_types.view_data_types"))
    return render_template("data_types/update_data_type.html", form=form)


@data_types.route("/data_type/<int:id>/delete", methods=["GET", "POST"])
def delete_data_type(id):
    data_type = DataType.query.get_or_404(int(id))
    db.session.delete(data_type)
    db.session.commit()
    flash("Session type deleted", category="success")
    return redirect(url_for("data_types.view_data_types"))
