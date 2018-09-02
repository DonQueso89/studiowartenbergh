from flask import render_template


def index():
    return render_template('home.html')


def contact():
    return render_template('contact.html')


def about():
    return render_template('about.html')


routes = (
    (index, '/'),
    (contact, '/contact'),
    (about, '/about'),
)
