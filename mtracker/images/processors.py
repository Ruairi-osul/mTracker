import os
from pathlib import Path
from mtracker.models import Image
from secrets import token_hex


def copy_image(form_data, save_dir, file_name_size=25):
    """Takes image from a form, gives it a unique name,
    and copies it copies it to save_dir. Returns the copied file name"""

    # generate filename
    file_format = Path(form_data.filename).suffix
    fn = "first" + file_format
    while Image.query.filter_by(image_path=fn).first():
        fn = token_hex(file_name_size) + file_format

    form_data.save(os.path.join(save_dir, fn))

    return fn
