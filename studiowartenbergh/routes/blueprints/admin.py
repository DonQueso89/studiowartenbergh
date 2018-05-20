import os
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for,
    current_app as app,
)
from werkzeug.utils import secure_filename
from collections import defaultdict

from .auth import login_required

from studiowartenbergh.db import get_db

bp = Blueprint('admin', __name__, url_prefix='/admin')


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
        selected_content = dict(session.execute(
            'SELECT * FROM content WHERE id = ?',
            (content_id,)
        ).fetchone())

        selected_content['images'] = [
            dict(x) for x in session.execute(
                'SELECT * FROM image WHERE content_id = ? ',
                (content_id,)
            ).fetchall()
        ]

    content_list = session.execute('SELECT id, title from content').fetchall()
    return render_template(
        'admin_base.html',
        content_list=content_list,
        selected_content=selected_content
    )


def add_files(session, request, content_id):
    """
    Add files to the filesystem where necessary.
    Add entries to the db for the corresponding content.
    """
    for img in request.files.getlist('image'):
        fname = secure_filename(img.filename)
        abspath = os.path.join(app.static_folder, fname)

        # File to filesystem
        if not os.path.isfile(abspath):
            img.save(abspath)

            # Entry in db
            session.execute(
                'INSERT INTO image (content_id, filename) VALUES (?, ?)',
                (content_id, fname)
            )
            session.commit()
            print("ADDED FILENAME: ", fname)


@bp.route('/submit_content', methods=['POST'])
@login_required
def submit_content():
    """
    Endpoint for creating or modifying content
    """
    create = request.form['content_id'] == ''
    session = get_db()

    if create:
        session.execute(
            'INSERT INTO content (title, body)'
            'VALUES (?, ?)',
            (request.form['title'], request.form['body'])
        )
        session.commit()

    content_id = session.execute(
        'SELECT id FROM content WHERE title = ?',
        (request.form['title'],)  # Title is unique
    ).fetchone()['id']

    if not create:
        session.execute(
            'UPDATE content SET title = ?, body = ?'
            'WHERE id = ?',
            (request.form['title'], request.form['body'], content_id)
        )
        session.commit()

    add_files(session, request, content_id)

    return redirect(url_for('admin.index'))
