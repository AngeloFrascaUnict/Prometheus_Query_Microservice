import functools

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session, jsonify
from flask import url_for
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from flask import current_app as app

# importing ObjectId from bson library
from bson import json_util, ObjectId
import json

# import MongoEngine models
from .models import User

# Blueprint Configuration
auth_bp = Blueprint(
    'auth_bp', __name__,
    template_folder='templates',
    static_folder='static'
    , url_prefix='/auth'
)


# se usiamo questo decoratore nelle route 
# obblighiamo l'utente ad effettuare un login prima
def login_required(view):
    """View decorator that redirects anonymous users to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth_bp.login"))

        return view(**kwargs)

    return wrapped_view

# carica lo user di sessione in g
@auth_bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from the database into ``g.user``."""
    user_id = session.get("user_id")
    
    if user_id is None:
        g.user = None
    else:
        g.user = User.objects(pk=user_id).first()



### ROUTES per questo Blueprint

@auth_bp.route('/', methods=['GET'])
@auth_bp.route('/index/', methods=['GET'])
def auth_index_function():
    return render_template("auth_index.html")


@auth_bp.route('/register/', methods=['GET', 'POST'])        
def register():
    """Register a new user.
    Validates that the username is not already taken. Hashes the password for security.
    """
    if request.method == "POST":
        username_r = request.form["username"]
        password_r = request.form["password"]

        error = None

        if not username_r:
            error = "Username is required."
        elif not password_r:
            error = "Password is required."

        if error is None:
            user = User.objects(username=username_r).first()

            if not user is None:
                error = f"User '{username_r}' is already registered."

            else:
                newuser = User(username=username_r, password=generate_password_hash(password_r))
                newuser.save()

                # Success, go to the login page.
                return redirect(url_for("auth_bp.login"))            

            flash(error)

    return render_template("register.html",
    title="Sign up", description="Sign up page")


@auth_bp.route("/login/", methods=["GET", "POST"])
def login():
    """Log in a registered user by adding the user id to the session."""
    if request.method == "POST":
        username_r = request.form["username"]
        password_r = request.form["password"]

        error = None

        user = User.objects(username=username_r).first()

        if user is None:
            error = "Incorrect username."

        elif not check_password_hash(user["password"], password_r):
            error = "Incorrect password."

        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            session.permanent = False
            session["user_id"] = json.loads(json_util.dumps(user.pk))['$oid']

            return redirect(url_for("prometheus_bp.prometheus_index"))            

        flash(error)

    return render_template("login.html",
    title="Sign in", description="Sign in page")


@login_required
@auth_bp.route("/logout/", methods=["GET", "POST"])
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("home_bp.home_index_function"))



# viene usata se usiamo una route errata!
# vedi : https://flask.palletsprojects.com/en/1.1.x/patterns/errorpages/
@auth_bp.errorhandler(404)
@login_required
def resource_not_found(e):

    return jsonify(error=str(e)), 404