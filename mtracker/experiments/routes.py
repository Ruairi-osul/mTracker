from flask import Blueprint, url_for, redirect, render_template, flash, request
from sqlalchemy.exc import IntegrityError
from mtracker.experiments.forms import AddExperimentForm, UpdateExperimentForm
from mtracker.models import Experiment
from mtracker.extentions import db

experiments = Blueprint("experiments", __name__)


@experiments.route("/view_experiments", methods=["GET", "POST"])
def view_experiments():
    page = request.args.get("page", 1, type=int)
    experiments = Experiment.query.paginate(per_page=20, page=page)
    return render_template("view_experiments.html", page=page, experiments=experiments)


@experiments.route("/experiment/add", methods=["GET", "POST"])
def add_experiment():
    form = AddExperimentForm()
    if form.validate_on_submit():
        new_experiment = Experiment(
            exp_name=form.exp_name.data, exp_description=form.exp_description.data
        )
        db.session.add(new_experiment)
        db.session.commit()
        flash(f"Experiment '{new_experiment.exp_name}' added.", category="success")
        return redirect(url_for("experiments.view_experiments"))
    return render_template("add_experiment.html", form=form)


@experiments.route("/experiment/<int:id>", methods=["GET", "POST"])
def single_experiment(id):
    exp = Experiment.query.get_or_404(int(id))
    return render_template("experiment.html", experiment=exp)


@experiments.route("/experiment/<int:id>/update", methods=["GET", "POST"])
def update_experiment(id):
    exp = Experiment.query.get_or_404(int(id))
    form = UpdateExperimentForm()
    if request.method == "GET":
        form.exp_name.data = exp.exp_name
        form.exp_description = exp.exp_description
    if form.validate_on_submit():
        exp.exp_name = form.exp_name.data
        exp.exp_description = form.exp_description.data
        try:
            db.session.add(exp)
            db.session.commit()
        except IntegrityError:
            flash(
                f"An experiment with name '{exp.exp_name}' already exists.",
                category="danger",
            )
            db.session.rollback()
            return redirect(url_for("update_experiment"), id=id)
        flash(f"Sucesfully updataed experiment '{exp.exp_name}'", category="success")
        return redirect(url_for("view_experiments"))
    return render_template("update_experiment.html", form=form)
