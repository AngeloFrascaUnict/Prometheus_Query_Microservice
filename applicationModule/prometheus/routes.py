from flask import Blueprint
from flask import render_template
from flask import current_app as app

# Blueprint Configuration
prometheus_bp = Blueprint(
    'prometheus_bp', __name__,
    template_folder='templates',
    static_folder='static'
)



### ROUTES per questo Blueprint

@prometheus_bp.route('/prometheus', methods=['GET'])
def home():
    """Prometheuspage."""

    return "ciao Prometheus page"