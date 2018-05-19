from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from collections import defaultdict

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    """
    Template that renders a list of content items and
    a modification / creation form.
    Optionally populates form with content data.
    """
    selected_content = defaultdict("")
    content_id = request.form['content_id']
    if request.method == 'POST':
        session = get_db()
        selected_content = session.execute(
            'SELECT * from content where id = ?',
            (content_id,)
        ).fetchall()
    return render_template('admin_base.html', selected_content=selected_content)


@bp.route('/submit_post', methods=['POST'])
@login_required
def submit_post():
    """
    Endpoint for creating or modifying content
    """
    return render_template('admin_base.html')
