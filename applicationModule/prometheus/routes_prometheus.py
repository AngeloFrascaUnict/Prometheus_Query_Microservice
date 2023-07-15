from flask import Blueprint
from flask import request, jsonify, abort, render_template
from flask import current_app as app

# parsing data Python (Dict, List) <-> JSON : json.dumps(x)
# y = json.loads(x) con x un JSON : Convert from JSON to Python
# y = json.dumps(x) con x un dict : Convert from Python to JSON
import json  

# libreria per gestire le date
import datetime
from datetime import datetime

# serve a convertire i cursor restituiti dalle aggregation in JSON                  
from bson import json_util

# import MongoEngine models
from .models import PrometheusQueriesResult, Data, Result, Metric

#
from ..auth.routes_auth import login_required

# Blueprint Configuration
prometheus_bp = Blueprint(
    'prometheus_bp', __name__,
    template_folder='templates',
    static_folder='static'
    , url_prefix='/prometheus'
)



### ROUTES per questo Blueprint

@login_required
@prometheus_bp.route('/', methods=['GET'])
@prometheus_bp.route('/index/', methods=['GET'])
def prometheus_index():

    return render_template("prometheus_index.html",
    title="Index", description="Prometheus index page")



# GET for getting data from Prometheus queries, passing formDateTime : YYYYMMDD:HHmm
@prometheus_bp.route('/api/data/', methods=['GET'])
@prometheus_bp.route('/api/data/<string:fromDateTime>', methods=['GET'])
@login_required
def get_query_prometheus_results(fromDateTime=None):

    if fromDateTime == None :
        data = PrometheusQueriesResult.objects()
    else :
        # constructor : datetime.datetime(year, month, day, [hour], [minute], [second], [microsecond], [tzone])
        fromDateTimeFormatted = datetime.datetime(int(fromDateTime[0:4]), int(fromDateTime[4:6]), int(fromDateTime[6:8])
            , int(fromDateTime[9:11]), int(fromDateTime[11:13]))

        data = PrometheusQueriesResult.objects(created_at__gt=fromDateTimeFormatted)

    if data is None:
        abort(404, description="Dati inesistenti")
    else:
        #return jsonify(data.to_json())
        return render_template('query_prometheus.html',
        title="Dati archiviati",
        description="queries response prometheus",
        data=data
        )


# viene usata se usiamo una route errata !
# vedi : https://flask.palletsprojects.com/en/1.1.x/patterns/errorpages/
@prometheus_bp.errorhandler(404)
@login_required
def resource_not_found(e):

    return jsonify(error=str(e)), 404

### FINE ROUTES per questo Blueprint





# Jinjia filters
@prometheus_bp.app_template_filter('datefromtimestamp')
def convert_timestamp_to_date(s):
    return datetime.fromtimestamp(s)

@prometheus_bp.app_template_filter('formatdatetime')
def format_date_time(s):
    return s.strftime("%m/%d/%Y, %H:%M:%S")




























    if firstname == None :
        user = None
    else :
        user = User.objects(firstname=firstname).first()

    if user is None:
        abort(404, description="User inesistente")
    else:
        user.delete()

    return jsonify(user.to_json())







