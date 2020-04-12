from flask import Blueprint, url_for, redirect, render_template, flash, request
from sqlalchemy.exc import IntegrityError
from mtracker.models import Group
from mtracker.extentions import db
from mtracker.groups.forms import AddGroupForm, UpdateGroupForm


groups = Blueprint("groups", __name__)


@groups.route("/view_groups", methods=["GET", "POST"])
def view_groups():
    page = request.args.get("page", 1, type=int)
    groups = Group.query.paginate(per_page=20, page=page)
    return render_template("groups/view_groups.html", page=page, groups=groups)


@groups.route("/group/add", methods=["GET", "POST"])
def add_group():
    form = AddGroupForm()
    if form.validate_on_submit():
        new_group = Group(
            group_name=form.group_name.data,
            group_description=form.group_description.data,
            experiment=form.experiment.data,
            genotype=form.genotype.data,
            sessions=form.sessions.data,
            surgeries=form.surgeries.data,
            data_types=form.data_types.data,
        )
        db.session.add(new_group)
        db.session.commit()
        flash(f"Group '{new_group.group_name}' added.", category="success")
        return redirect(url_for("groups.view_groups"))
    return render_template("groups/add_group.html", form=form)


@groups.route("/group/<int:id>", methods=["GET", "POST"])
def single_group(id):
    group = Group.query.get_or_404(int(id))
    return render_template("groups/group.html", group=group)


@groups.route("/group/<int:id>/update", methods=["GET", "POST"])
def update_group(id):
    group = Group.query.get_or_404(int(id))
    form = UpdateGroupForm()
    if request.method == "GET":
        form.group_name.data = group.group_name
        form.group_description.data = group.group_description
        form.genotype.data = group.genotype
        form.sessions.data = group.sessions
        form.surgeries.data = group.surgeries
        form.data_types.data = group.data_types
    if form.validate_on_submit():
        group.group_name = form.group_name.data
        group.group_description = form.group_description.data
        group.genotype = form.genotype.data
        group.sessions = form.sessions.data
        group.surgeries = form.surgeries.data
        group.data_types = form.data_types.data
        try:
            db.session.add(group)
            db.session.commit()
        except IntegrityError:
            flash(
                f"A session type with name '{group.group_name}' already exists.",
                category="danger",
            )
            db.session.rollback()
            return redirect(url_for("update_group"), id=id)
        flash(
            f"Sucesfully updataed group '{group.group_name}'", category="success",
        )
        return redirect(url_for("groups.view_groups"))
    return render_template("groups/update_group.html", form=form)


@groups.route("/group/<int:id>/delete", methods=["GET", "POST"])
def delete_group(id):
    group = Group.query.get_or_404(int(id))
    db.session.delete(group)
    db.session.commit()
    flash("Session type deleted", category="success")
    return redirect(url_for("groups.view_groups"))
