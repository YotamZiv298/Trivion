from flask import render_template, Blueprint
from flask_login import login_required

main = Blueprint("main", __name__)

HOME = "Home.html"
ABOUT = "About.html"


@main.route("/home")
@login_required
def home():
    """
    Home page route
    :return: Home.html template
    """
    return render_template(HOME)


@main.route("/about")
def about():
    """
    About page route
    :return: About.html template
    """
    return render_template(ABOUT, title="About")
