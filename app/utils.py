import os
import secrets
from flask import current_app


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def save_picture(form_picture_file):
    if not form_picture_file or form_picture_file.filename == '':
        return None

    if allowed_file(form_picture_file.filename):
        random_hex = secrets.token_hex(8)
        _, f_ext = os.path.splitext(form_picture_file.filename)
        picture_fn = random_hex + f_ext
        picture_path = os.path.join(current_app.config['UPLOAD_FOLDER'], picture_fn)

        form_picture_file.save(picture_path)
        return picture_fn
    return None