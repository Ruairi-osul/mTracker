from flask import (
    Blueprint,
    url_for,
    redirect,
    render_template,
    flash,
    request,
    current_app,
)
from mtracker.models import Image, Mouse
from mtracker.extentions import db
from mtracker.images.forms import AddImageForm
from mtracker.images.processors import copy_image
import os


images = Blueprint("images", __name__)


@images.route("/view_images", methods=["GET", "POST"])
def view_images():
    page = request.args.get("page", 1, type=int)
    images = Image.query.paginate(per_page=20, page=page)
    return render_template("images/view_images.html", page=page, images=images)


@images.route("/image/add", methods=["GET", "POST"])
def add_image():
    IMAGE_SAVE_DIR = os.path.join(current_app.root_path, "static", "uploaded_images")
    form = AddImageForm()
    if request.method == "GET":
        if request.args.get("m_id"):
            form.mouse.data = Mouse.query.get(int(request.args["m_id"]))
    if form.validate_on_submit():
        image_path = copy_image(
            form_data=form.image_file.data, save_dir=IMAGE_SAVE_DIR, file_name_size=25,
        )
        new_image = Image(
            image_name=form.image_name.data,
            image_path=image_path,
            mouse=form.mouse.data,
        )
        db.session.add(new_image)
        db.session.commit()
        flash(f"Image '{new_image.image_name}' added.", category="success")
        return redirect(url_for("images.view_images"))
    return render_template("images/add_image.html", form=form)


@images.route("/image/<int:id>", methods=["GET", "POST"])
def single_image(id):
    image = Image.query.get_or_404(int(id))
    return render_template("images/image.html", image=image)


@images.route("/image/<int:id>/delete", methods=["GET", "POST"])
def delete_image(id):
    IMAGE_SAVE_DIR = os.path.join(current_app.root_path, "static", "uploaded_images")
    image = Image.query.get_or_404(int(id))
    os.remove(os.path.join(IMAGE_SAVE_DIR, image.image_path))
    db.session.delete(image)
    db.session.commit()
    flash("Session type deleted", category="success")
    return redirect(url_for("images.view_images"))
