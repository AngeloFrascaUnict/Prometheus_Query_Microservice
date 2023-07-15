from flask import Blueprint
from flask import render_template
from flask import current_app as app

# Blueprint Configuration
home_bp = Blueprint(
    'home_bp', __name__,
    template_folder='templates',
    static_folder='static'
    , url_prefix='/home'
)


### ROUTES per questo Blueprint

@home_bp.route('/', methods=['GET'])
@home_bp.route('/index/', methods=['GET'])
def home_index_function():
    """Homepage."""

    return render_template('home_index.html',
        title="Home page",
        description="Home page",

        )