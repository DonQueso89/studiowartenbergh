def index():
    return """
        <h1>Hello World</h1>
        <ul>
        <li><a href="/aboutme">About me</a></li>
        <li><a href="/aboutmystuff">About my stuff</a></li>
        </ul>
    """


def about_me():
    return """
        <h1>I am awesome</h1>
        <ul>
        <li><a href="/">Home</a></li>
        </ul>
    """


def about_my_stuff():
    return """
        <h1>My stuff is awesome</h1>
        <ul>
        <li><a href="/">Home</a></li>
        </ul>
    """


routes = (
    (index, '/'),
    (about_me, '/aboutme'),
    (about_my_stuff, '/aboutmystuff'),

)
