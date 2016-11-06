import sys, os, sqlite3
from markdown import markdown
from flask import g, request, Response, jsonify
from flask_api import FlaskAPI, status

# Allow script run on shell (local files for PYTHONPATH)
sys.path.append(os.path.join(os.getcwd(),os.path.dirname(__file__), '../'))
from client.emission import Emission
from client.errorhandlers import InvalidUsage
from complexresponse import ComplexResponse
import settings as s
from validator import EmissionValidator, QueryParameterValidator

app = FlaskAPI(__name__)
app.url_map.strict_slashes = False

########################
# Database Manipulation
########################
def make_dicts(cursor, row):
    """ This function converts a sqlite row into a key value dictionary.
    """
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

def get_db():
    """ Returns a connection object used to access the sqlite database.
    """
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(s.DATABASE_PATH)
        db.row_factory = make_dicts
    return db

@app.teardown_appcontext
def close_connection(exception):
    """ Close the database connection automatically if the application is closed.
    """
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    """ Create the emission table using a provided schema.
    """
    with app.app_context():
        db = get_db()
        with app.open_resource(s.DATABASE_SCHEMA_PATH, mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def query_db(query, args=(), just_one=False):
    """ Executes a query string and return the resulting rows.
    If just_one flag is set to true, return only the first returned row.
    """
    with app.app_context():
        cursor = get_db().execute(query, args)
        get_db().commit()
        rows = cursor.fetchall()
        cursor.close()
        return (rows[0] if rows else None) if just_one else rows

def query_db_insert(query, args=()):
    """ Executes a query insert string and return the last inserted id.
    """
    with app.app_context():
        cursor = get_db().execute(query, args)
        get_db().commit()
        lastrowid = cursor.lastrowid
        cursor.close()
        return lastrowid

def add_emission(emission = Emission()):
    """ Use the emission object in a sql query insert. If successful return the
    row insert id.
    """
    return query_db_insert("INSERT INTO emissions(vehicleId, vehicleType, latitude, longitude, timestamp, heading) VALUES(?,?,?,?,?,?)", 
                    (str(emission.vehicle_id), str(emission.vehicle_type), 
                     emission.latitude, emission.longitude, emission.timestamp, 
                     emission.heading))

def get_emissions_by_vehicle_id(vehicle_id, offset=None, limit=None):
    """ Returns a list of existing emissions based in the input vehicle id.
    If limit is not provide, all emissions from that vehicle id are returned.
    """
    sql_query = """SELECT vehicleId, vehicleType, latitude, longitude, 
                    timestamp, heading 
                    FROM emissions 
                    WHERE vehicleId = :vehicle_id
    """
    sql_query_count = """SELECT COUNT(*) as total 
                    FROM emissions 
                    WHERE vehicleId = :vehicle_id;
    """
    args = {'vehicle_id': str(vehicle_id)}
    total = query_db(sql_query_count, args, True)
    if limit:
        sql_query += ' ORDER BY vehicleId '
        args['limit'] = limit
        if offset:
            sql_query += ' LIMIT :offset, :limit'
            args['offset'] = offset
        else:
            sql_query += ' LIMIT :limit'
    sql_query_count += ';'

    return (total['total'], query_db(sql_query, args))

def get_emissions_by_vehicle_type(vehicle_type, offset=None, limit=None):
    """ Returns a list of existing emissions based in the input vehicle type.
    If limit is not provide, all emissions from that vehicle type are returned.
    """
    sql_query = """SELECT vehicleId, vehicleType, latitude, longitude, 
                    timestamp, heading 
                    FROM emissions 
                    WHERE vehicleType = :vehicle_type
    """
    sql_query_count = """SELECT COUNT(*) as total 
                    FROM emissions 
                    WHERE vehicleType = :vehicle_type;
    """
    args = {'vehicle_type': str(vehicle_type)}
    total = query_db(sql_query_count, args, True)
    if limit:
        sql_query += ' ORDER BY vehicleId '
        args['limit'] = limit
        if offset:
            sql_query += ' LIMIT :offset, :limit'
            args['offset'] = offset
        else:
            sql_query += ' LIMIT :limit'
    sql_query_count += ';'

    return (total['total'], query_db(sql_query, args))

def get_emissions(offset=None, limit=None):
    """ Returns a list containing all existing emissions.
    If limit is not provide, all emissions from that vehicle are returned.
    """
    sql_query = """SELECT vehicleId, vehicleType, latitude, longitude, 
                    timestamp, heading 
                    FROM emissions
    """
    sql_query_count = """SELECT COUNT(*) as total 
                    FROM emissions;
    """
    args = {}
    total = query_db(sql_query_count, args, True)
    if limit:
        sql_query += ' ORDER BY vehicleId '
        args['limit'] = limit
        if offset:
            sql_query += ' LIMIT :offset, :limit'
            args['offset'] = offset
        else:
            sql_query += ' LIMIT :limit'
    sql_query_count += ';'

    return (total['total'], query_db(sql_query, args))

################
# API Endpoints
################
@app.route(s.ROOT_PATH, methods=['GET'])
def app_root():
    """ Allows access to GET at root site level. This return if it can the readme 
    documentation for this tool.
    """
    try:
        with open(s.README_STATIC_PATH, 'r') as f:
            return Response(markdown(f.read()), mimetype='text/html'), status.HTTP_200_OK
    except:
        return Response('Hello World!', mimetype='text/html'), status.HTTP_200_OK

@app.route(s.EMISSIONS_PATH, methods=['POST'])
def collect_emissions():
    """ Allows access to POST an emission. If emission is valid, try to save 
    it at database. Returns a response object containing the current emission
    converted to json, and also the header that allows access to that vehicle 
    emissions directly.
    """
    ev = EmissionValidator()
    data = ev.validate_emission_input_data(request.get_json())
    emission = Emission(data['vehicle_id'], data['vehicle_type'],
                        data['latitude'], data['longitude'],
                        data['timestamp'], data['heading'])

    add_emission(emission)
    response = jsonify(emission.generate_output())
    response.status_code = status.HTTP_201_CREATED
    response.headers['location'] = s.VEHICLES_PATH + str(data['vehicle_id']) +'/'
    return response

@app.route(s.VEHICLES_PATH + '<uuid:vehicle_id>', methods=['GET'])
def show_emissions_by_vehicle_id(vehicle_id):
    """ Allows access to GET emissions by vehicle id. Returns a response 
    ready for pagination control.
    """
    qpv = QueryParameterValidator()
    offset, limit = qpv.validate_query_parameters(request)
    total, result = get_emissions_by_vehicle_id(vehicle_id, offset, limit)
    cr = ComplexResponse(total, offset, limit, result)
    response = jsonify(cr.generate_output())
    response.status_code = status.HTTP_200_OK
    return response

@app.route(s.VEHICLES_TYPE_PATH + '<string:vehicle_type>', methods=['GET'])
def show_emissions_by_vehicle_type(vehicle_type):
    """ Allows access to GET emissions by vehicle type. Returns a response 
    ready for pagination control.
    """
    qpv = QueryParameterValidator()
    offset, limit = qpv.validate_query_parameters(request)
    total, result = get_emissions_by_vehicle_type(vehicle_type, offset, limit)
    cr = ComplexResponse(total, offset, limit, result)
    response = jsonify(cr.generate_output())
    response.status_code = status.HTTP_200_OK
    return response

@app.route(s.EMISSIONS_PATH, methods=['GET'])
def show_emissions():
    """ Allows access to GET emissions. Returns a response ready for pagination 
    control.
    """
    qpv = QueryParameterValidator()
    offset, limit = qpv.validate_query_parameters(request)
    total, result = get_emissions(offset, limit)
    cr = ComplexResponse(total, offset, limit, result)
    response = jsonify(cr.generate_output())
    response.status_code = status.HTTP_200_OK
    return response

@app.errorhandler(InvalidUsage)
def handle_invalid_input(error):
    """ Catch all app exceptions and return an appropriate response using its 
    exception message.
    """
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

if __name__ == '__main__':
    # initialize database
    init_db()
    app.run(threaded=True, debug=s.DEFAULT_FLASK_DEBUG_MODE, 
            host=s.DEFAULT_FLASK_EXTERNAL_HOST, port=s.DEFAULT_FLASK_PORT)
