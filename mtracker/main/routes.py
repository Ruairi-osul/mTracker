from flask import Blueprint, render_template

main = Blueprint("main", __name__)


@main.route("/")
@main.route("/home")
def index():
    return render_template("index.html")


@main.route("/add_entry")
def add_entry():
    return render_template("add_entry.html")


@main.route("/view_entries")
def view_entries():
    return render_template("view_entries.html")


@main.route("/quickstart")
def quickstart():
    return render_template("quickstart.html")


@main.route("/datamodel")
def datamodel():
    return render_template("datamodel.html")
