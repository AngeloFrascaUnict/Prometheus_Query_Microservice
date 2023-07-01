from flask import current_app as app
from flask import make_response, jsonify, render_template

@app.route("/api/v2/test_response")

#def users():
    # headers = {"Content-Type": "application/json"}
    # return make_response(
    #     jsonify('Test worked!'),
    #     200,
    #     headers=headers
    # )


# def index():
#   myResponse = make_response('Response')
#   myResponse.headers['customHeader'] = 'This is a custom header'
#   myResponse.status_code = 403
#   myResponse.mimetype = 'video/mp4'

#   return myResponse 

@app.route("/")
def home():
    """Serve homepage template."""
    return render_template("index.html")