from flask import Blueprint
from flask import request, jsonify, abort, render_template
from flask import current_app as app

# parsing data Python (Dict, List) <-> JSON : json.dumps(x)
# y = json.loads(x) con x un JSON : Convert from JSON to Python
# y = json.dumps(x) con x un dict : Convert from Python to JSON
import json  

# libreria per gestire le date
import datetime

# serve a convertire i cursor restituiti dalle aggregation in JSON                  
from bson import json_util

# import models
from .modelsold import User, Customer

from .models import QueryResultVector, DataVector, ResultVector, Metric
from .models import QueryResultMatrix, DataMatrix, ResultMatrix



# Blueprint Configuration
prometheus_bp = Blueprint(
    'prometheus_bp', __name__,
    template_folder='templates',
    static_folder='static'
)



### ROUTES per questo Blueprint

@prometheus_bp.route('/prometheus', methods=['GET'])
def home_prometheus_page():

    return "Hi all by Prometheus page!"



# GET for getting data from Prometheus queries, passing formDateTime : YYYYMMDD:HHmm
@app.route('/prometheus/api/data/', methods=['GET'])
@app.route('/prometheus/api/data/<string:fromDateTime>', methods=['GET'])
def get_query_prometheus_results(fromDateTime=None):

    if fromDateTime == None :
        data = QueryResultVector.objects()
    else :
        # constructor : datetime.datetime(year, month, day, [hour], [minute], [second], [microsecond], [tzone])
        fromDateTimeFormatted = datetime.datetime(int(fromDateTime[0:4]), int(fromDateTime[4:6]), int(fromDateTime[6:8])
            , int(fromDateTime[9:11]), int(fromDateTime[11:13]))

        data = QueryResultVector.objects(created_at__gt=fromDateTimeFormatted)
        
    if data is None:
        abort(404, description="Dati inesistenti")
    else:
        return jsonify(data.to_json())






















# GET for getting User/Users
@app.route('/prometheus/api/users/', methods=['GET'])
@app.route('/prometheus/api/users/<string:firstname>', methods=['GET'])
def get_query_results(firstname=None):

    if firstname == None :
        users = User.objects()
    else :
        users = User.objects(firstname=firstname).first()
        
    if users is None:
        abort(404, description="User inesistente")
    else:
        return jsonify(users.to_json())


# PUT for update User : i dati sono passati da una Form
@app.route('/prometheus/api/users/update', methods=['PUT'])
def update_user():

    #1. in questa maniera i dati devono essere passati in modalità Raw e JSON da postman
    #record = json.loads(request.data)     
    #user = User(firstname=record['firstname'], lastname=record['lastname'])

    #2. in questa maniera i dati devono essere passati in modalità x-www-from-urlencoded da postman
    users = User.objects(firstname=request.form.get('firstname'))

    if users is None:
        abort(404, description="User inesistente")
    else:
        users.update_one(lastname=request.form.get('lastname'))

    return jsonify(users.first().to_json())


# POST for create User : i dati sono passati da una Form
@app.route('/prometheus/api/users/create', methods=['POST'])
def create_user():

    #1. in questa maniera i dati devono essere passati in modalità Raw e JSON da postman
    #record = json.loads(request.data)     
    #user = User(firstname=record['firstname'], lastname=record['lastname'])

    #2. in questa maniera i dati devono essere passati in modalità x-www-from-urlencoded da postman
    user = User(firstname=request.form.get('firstname'), lastname=request.form.get('lastname'))
    
    user.save()

    return jsonify(user.to_json())


# DELETE for deleting User
@app.route('/prometheus/api/users/delete/<string:firstname>', methods=['DELETE'])
def delete_record(firstname):

    if firstname == None :
        user = None
    else :
        user = User.objects(firstname=firstname).first()

    if user is None:
        abort(404, description="User inesistente")
    else:
        user.delete()

    return jsonify(user.to_json())





# vedi : https://flask.palletsprojects.com/en/1.1.x/patterns/errorpages/
@app.errorhandler(404)
def resource_not_found(e):

    return jsonify(error=str(e)), 404


