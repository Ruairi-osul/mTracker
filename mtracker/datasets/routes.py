from flask import Blueprint, request, render_template, redirect, flash, url_for
from mtracker.datasets.forms import AddDataSetForm
from mtracker.models import DataSet, Mouse
from mtracker.datasets.processors import processor_factory, ProcessingError
from mtracker.datasets.inserters import inserter_factory
from mtracker.datasets.utils import data_query_factory, dset_template_factory
from mtracker.extentions import db

datasets = Blueprint("datasets", __name__)


@datasets.route("/datasets/add", methods=["GET", "POST"])
def add_dataset():
    form = AddDataSetForm()
    if request.method == "GET":
        m_id = request.args.get("m_id", None)
        if m_id:
            if Mouse.query.get(m_id):
                form.mouse.data = Mouse.query.get(m_id)
    if form.validate_on_submit():
        new_dataset = DataSet(
            mouse=form.mouse.data,
            data_type=form.data_type.data,
            session=form.session.data,
        )
        db.session.add(new_dataset)
        db.session.flush()
        processor = processor_factory(category=new_dataset.data_type.category)
        inserter = inserter_factory(category=new_dataset.data_type.category)
        try:
            dataset_data = processor.process_data(
                form.datafile.data, dset_id=new_dataset.id
            )
            inserter.insert_data(dataset_data, db.session)
            db.session.commit()
            return redirect(url_for("datasets.view_datasets"))
        except ProcessingError as e:
            print(e)
            flash("Error Processing Dataset", category="danger")
            db.session.rollback()
            return redirect(url_for("datasets.add_dataset"))
    return render_template("datasets/add_dataset.html", form=form)


@datasets.route("/datasets/view")
def view_datasets():
    page = request.args.get("page", 1, type=int)
    dsets = DataSet.query.paginate(per_page=20, page=page)
    return render_template("datasets/view_datasets.html", dsets=dsets, page=page)


@datasets.route("/datasets/<int:id>")
def single_dataset(id):
    dset = DataSet.query.get_or_404(id)
    data_query = data_query_factory(
        dset_id=dset.id, data_category=dset.data_type.category
    )
    print(dset.data_type)
    print("UP")
    page = request.args.get("page", 1, int)
    data = data_query.paginate(per_page=20, page=page)
    template = dset_template_factory(data_category=dset.data_type.category)
    return render_template(template, data=data, dset=dset)


@datasets.route("/datasets/<int:id>/delete", methods=["GET", "POST"])
def delete_dataset(id):
    dset = DataSet.get_or_404(id)
    db.session.delete(dset)
    db.session.commit()
    flash("Dataset deleted.", category="success")
    return redirect(url_for("datasets.view_datasets"))
