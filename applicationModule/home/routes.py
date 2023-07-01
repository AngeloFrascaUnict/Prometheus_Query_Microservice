from flask import Blueprint
from flask import render_template
from flask import current_app as app

#from flask_blueprint_tutorial.api import fetch_products

# Blueprint Configuration
home_bp = Blueprint(
    'home_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


### ROUTES per questo Blueprint

# @home_bp.route('/', methods=['GET'])
# def home():
#     """Homepage."""
#     products = fetch_products(app)
#     return render_template(
#         'index.jinja2',
#         title='Flask Blueprint Demo',
#         subtitle='Demonstration of Flask blueprints in action.',
#         template='home-template',
#         products=products
#     )

@home_bp.route('/home', methods=['GET'])
def home():
    """Homepage."""

    return "ciao Home page"