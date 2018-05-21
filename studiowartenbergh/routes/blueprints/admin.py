import os
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for,
    current_app as app,
)
from werkzeug.utils import secure_filename
from sqlite3 import IntegrityError
from collections import defaultdict

from .auth import login_required

from studiowartenbergh.db import get_db

bp = Blueprint('admin', __name__, url_prefix='/admin')


def content_id_from_title(session, title):
    return session.execute(
        'SELECT id FROM content WHERE title = ?',
        (request.form['title'], )  # title is unique
    ).fetchone()['id']


def content_from_id(session, content_id):
    result = dict(session.execute(
        'SELECT * FROM content WHERE id = ?',
        (content_id,)
    ).fetchone())

    result['images'] = [
        dict(x) for x in session.execute(
            'SELECT * FROM image WHERE content_id = ? ',
            (content_id,)
        ).fetchall()
    ]

    return result


def content_list(session):
    return session.execute('SELECT id, title from content').fetchall()


def add_images(session, request, content_id):
    """
    Add files to the filesystem where necessary.
    Queue entries to the db for the corresponding content.
    """
    for img in request.files.getlist('image'):
        fname = secure_filename(img.filename)
        abspath = os.path.join(app.static_folder, fname)

        if not os.path.isfile(abspath):
            img.save(abspath)

        try:
            session.execute(
                'INSERT INTO image (content_id, filename) VALUES (?, ?)',
                (content_id, fname)
            )
        except IntegrityError as e:
            # Image is already added to content
            print("Image added twice to content ", e)

    return session


def remove_images(session, image_ids):
    """
    Remove images from filesystem where necessary.
    Remove corresponding entries in db.

    :param session: sqlite3.Connection
    :param image_ids: list of image_ids
    """
    for image_id in image_ids:
        fname = session.execute(
            'SELECT filename FROM image WHERE id = ?',
            (image_id, )
        ).fetchone()['filename']

        last_item = session.execute(
            'SELECT COUNT(*) FROM image WHERE filename = ?',
            (fname,)
        ).fetchone()[0] <= 1

        session.execute(
            'DELETE FROM image WHERE id = ?',
            (image_id, )
        )

        # Only remove the file if its the last entry
        if last_item:
            abspath = os.path.join(app.static_folder, fname)

            if os.path.isfile(abspath):
                os.remove(abspath)

    return session


@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    """
    Template that renders a list of content items and
    a modification / creation form.
    Optionally populates form with content data.
    """
    selected_content = defaultdict(lambda: "")
    session = get_db()

    if request.method == 'POST':
        content_id = request.form['content_select']
        session = get_db()
        selected_content = content_from_id(session, content_id)

    _content_list = content_list(session)
    return render_template(
        'admin_base.html',
        content_list=_content_list,
        selected_content=selected_content
    )


@bp.route('/submit_content', methods=['POST'])
@login_required
def submit_content():
    """
    Endpoint for creating or modifying content
    """
    content_id = request.form['content_id']
    session = get_db()

    if content_id == '':
        session.execute(
            'INSERT INTO content (title, body)'
            'VALUES (?, ?)',
            (request.form['title'], request.form['body'])
        )
        session.commit()
        content_id = content_id_from_title(session, request.form['title'])
    else:
        session.execute(
            'UPDATE content SET title = ?, body = ?'
            'WHERE id = ?',
            (request.form['title'], request.form['body'], content_id)
        )
    session = add_images(session, request, content_id)
    session.commit()

    return render_template(
        'admin_base.html',
        content_list=content_list(session),
        selected_content=content_from_id(session, content_id)
    )


@bp.route('/<int:image_id>/<int:content_id>/delete_image', methods=['GET'])
def delete_image(image_id, content_id):
    session = get_db()
    session = remove_images(session, [image_id])
    session.commit()
    return render_template(
        'admin_base.html',
        content_list=content_list(session),
        selected_content=content_from_id(session, content_id)
    )


@bp.route('/delete_content', methods=['POST'])
def delete_content():
    content_id = request.form['content_id']

    session = get_db()
    session.execute("DELETE FROM content WHERE id = ?", (content_id, ))
    session = remove_images(session, request.form.getlist('image'))
    session.commit()

    return redirect(url_for('admin.index'))
