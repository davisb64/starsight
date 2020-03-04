from flask import Blueprint

star = Blueprint('star', __name__)

from . import views, forms
