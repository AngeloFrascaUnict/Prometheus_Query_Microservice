from flask import current_app as app
from flask import make_response, jsonify, render_template, session, redirect, url_for


@app.route("/")
def home():
    """Serve homepage template."""
    #return render_template("index.html")
    session.clear()
    return redirect(url_for("home_bp.home_index_function"))