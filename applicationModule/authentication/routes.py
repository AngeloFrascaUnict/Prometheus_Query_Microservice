from flask import Blueprint
from flask import render_template
from flask import current_app as app

#from flask_blueprint_tutorial.api import fetch_products

# Blueprint Configuration
auth_bp = Blueprint(
    'auth_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


### ROUTES per questo Blueprint

@auth_bp.route('/auth', methods=['GET'])
def auth():
    """Homepage."""

    return "ciao Auth page"