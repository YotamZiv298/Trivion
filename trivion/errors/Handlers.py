from flask import Blueprint, render_template

errors = Blueprint("errors", __name__)


@errors.app_errorhandler(404)
def error_404(error):
    """
    Error 404
    :param error: error
    :return: 404.html
    """
    return render_template("errors/404.html"), 404


@errors.app_errorhandler(403)
def error_403(error):
    """
    Error 403
    :param error: error
    :return: 403.html
    """
    return render_template("errors/403.html"), 403


@errors.app_errorhandler(500)
def error_500(error):
    """
    Error 500
    :param error: error
    :return: 500.html
    """
    return render_template("errors/500.html"), 500
