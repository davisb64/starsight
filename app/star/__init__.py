from flask import Blueprint

main = Blueprint('star', __name__)

from . import views, forms
