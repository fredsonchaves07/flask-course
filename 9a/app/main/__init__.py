from flask import Blueprint
from ..models import Permision

main = Blueprint('main', __name__)

@main.app_context_processor
def inject_permissions():
    return dict(Permision=Permision)

from . import views, erros