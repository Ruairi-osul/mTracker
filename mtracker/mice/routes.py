from flask import Blueprint, url_for, redirect, render_template, flash, request
from sqlalchemy.exc import IntegrityError
from mtracker.models import Mouse
from mtracker.extentions import db
from mtracker.mice.forms import AddMouseForm, UpdateMouseForm


mice = Blueprint("mice", __name__)


@mice.route("/view_mice", methods=["GET", "POST"])
def view_mice():
    page = request.args.get("page", 1, type=int)
    mice = Mouse.query.paginate(per_page=20, page=page)
    return render_template("mice/view_mice.html", page=page, mice=mice)


@mice.route("/mouse/add", methods=["GET", "POST"])
def add_mouse():
    form = AddMouseForm()
    if form.validate_on_submit():
        new_mouse = Mouse(
            mouse_name=form.mouse_name.data,
            dob=form.dob.data,
            cull_date=form.cull_date.data,
            is_done=form.is_done.data,
            group=form.group.data,
            is_male=form.is_male.data,
        )
        db.session.add(new_mouse)
        db.session.commit()
        flash(f"Mouse '{new_mouse.mouse_name}' added.", category="success")
        return redirect(url_for("mice.view_mice"))
    return render_template("mice/add_mouse.html", form=form)


@mice.route("/mouse/<int:id>", methods=["GET", "POST"])
def single_mouse(id):
    mouse = Mouse.query.get_or_404(int(id))
    return render_template("mice/mouse.html", mouse=mouse)


@mice.route("/mouse/<int:id>/update", methods=["GET", "POST"])
def update_mouse(id):
    mouse = Mouse.query.get_or_404(int(id))
    form = UpdateMouseForm()
    if request.method == "GET":
        form.mouse_name.data = mouse.mouse_name
        form.dob.data = mouse.dob
        form.cull_date.data = mouse.cull_date
        form.is_done.data = mouse.is_done
        form.group.data = mouse.group
        form.is_male.data = mouse.is_male
    if form.validate_on_submit():
        mouse.mouse_name = form.mouse_name.data
        mouse.dob = form.dob.data
        mouse.cull_date = form.cull_date.data
        mouse.is_done = form.is_done.data
        mouse.group = form.group.data
        mouse.is_male = form.is_male.data
        try:
            db.session.add(mouse)
            db.session.commit()
        except IntegrityError:
            flash(
                f"A session type with name '{mouse.mouse_name}' already exists.",
                category="danger",
            )
            db.session.rollback()
            return redirect(url_for("update_mouse"), id=id)
        flash(
            f"Sucesfully updataed mouse '{mouse.mouse_name}'", category="success",
        )
        return redirect(url_for("mice.view_mice"))
    return render_template("mice/update_mouse.html", form=form)


@mice.route("/mouse/<int:id>/delete", methods=["GET", "POST"])
def delete_mouse(id):
    mouse = Mouse.query.get_or_404(int(id))
    db.session.delete(mouse)
    db.session.commit()
    flash("Session type deleted", category="success")
    return redirect(url_for("mice.view_mice"))
