from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def error_404(error):
    """ 404 Error """
    return render_template('404.html'), 404


@errors.app_errorhandler(403)
def error_403(error):
    """ 403 Error """
    return render_template('403.html'), 403


@errors.app_errorhandler(500)
def error_500(error):
    """ 500 Error """
    return render_template('500.html'), 500