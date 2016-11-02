import sys, os, sqlite3, uuid, random, time
from uuid import UUID
from markdown import markdown
from flask import g, request, Response, jsonify
from flask_api import FlaskAPI, status
# Allow script run on shell (local files for PYTHONPATH)
sys.path.append(os.path.join(os.getcwd(),os.path.dirname(__file__), '../'))
from client.emission import Emission
from client.errorhandlers import InvalidUsage
from complexresponse import ComplexResponse

app = FlaskAPI(__name__)
app.url_map.strict_slashes = False

CURRENT_STATIC_PATH = os.path.dirname(os.path.abspath(__file__))
TOWN_CENTRE = {'latitude': 52.902700, 'longitude': -3.812850}
TOWN_BOUNDAIRES_RADIUS = 50000.0 # 50 km in meters
TOWN_BOUNDAIRES_SCALE = TOWN_BOUNDAIRES_RADIUS / 100000 # 0.5 max degree 
TOWN_BOUNDAIRES_BOX = {'north': TOWN_CENTRE['latitude'] + TOWN_BOUNDAIRES_SCALE,
                       'south': TOWN_CENTRE['latitude'] - TOWN_BOUNDAIRES_SCALE,
                       'west': TOWN_CENTRE['longitude'] - TOWN_BOUNDAIRES_SCALE,
                       'east': TOWN_CENTRE['longitude'] + TOWN_BOUNDAIRES_SCALE}
MIN_HEADING = 0
MAX_HEADING = 359
DEFAULT_OFFSET = 0
DEFAULT_LIMIT = 250

""" Database connection and manipulation
"""
DATABASE_PATH = CURRENT_STATIC_PATH + '/../db/snowdonia.db'
DATABASE_SCHEMA_PATH = CURRENT_STATIC_PATH + '/../db/schema.sql'

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE_PATH)
        db.row_factory = make_dicts
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource(DATABASE_SCHEMA_PATH, mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def query_db(query, args=(), just_one=False):
    """ Execute a query string and return the resulting rows.
    If just_one flag is true, return only the first row.
    """
    with app.app_context():
        cursor = get_db().execute(query, args)
        get_db().commit()
        rows = cursor.fetchall()
        cursor.close()
        return (rows[0] if rows else None) if just_one else rows

def query_db_insert(query, args=()):
    """ Execute a query insert string and return the last inserted id.
    """
    with app.app_context():
        cursor = get_db().execute(query, args)
        get_db().commit()
        lastrowid = cursor.lastrowid
        cursor.close()
        return lastrowid

# initialize database
init_db()

def add_emission(emission = Emission()):
    return query_db_insert("INSERT INTO emissions(vehicleId, vehicleType, latitude, longitude, timestamp, heading) VALUES(?,?,?,?,?,?)", 
                    (str(emission.vechicle_id), str(emission.vehicle_type), 
                     emission.latitude, emission.longitude, emission.timestamp, 
                     emission.heading))

def get_emissions_by_vehicle_id(vehicle_id, offset=None, limit=None):
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
    if limit:
        total = query_db(sql_query_count, args, True)
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
    if limit:
        total = query_db(sql_query_count, args, True)
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
    sql_query = """SELECT vehicleId, vehicleType, latitude, longitude, 
                    timestamp, heading 
                    FROM emissions
    """
    sql_query_count = """SELECT COUNT(*) as total 
                    FROM emissions;
    """
    args = {}
    if limit:
        total = query_db(sql_query_count, args, True)
        sql_query += ' ORDER BY vehicleId '
        args['limit'] = limit
        if offset:
            sql_query += ' LIMIT :offset, :limit'
            args['offset'] = offset
        else:
            sql_query += ' LIMIT :limit'
    sql_query_count += ';'

    return (total['total'], query_db(sql_query, args))

""" API endpoints manipulation
"""

ROOT_PATH = '/'
API_VERSION = '1' # Please use simple ordinal there
API_ROOT_PATH = ROOT_PATH + 'api/v' + API_VERSION + '/'
EMISSIONS_PATH = API_ROOT_PATH + 'emissions/'
VEHICLES_PATH = EMISSIONS_PATH + 'vehicles/'
VEHICLES_TYPE_PATH = VEHICLES_PATH + 'type/'
README_STATIC_PATH = CURRENT_STATIC_PATH + '/../README.md'

def generate_mock_emission():
    return {'vehicle_id': uuid.uuid4(), 
            'vehicle_type': random.choice(['bus', 'taxi', 'tram', 'train']),
            'latitude':round(random.uniform(-90, 90), 6),
            'longitude':round(random.uniform(-180, 180), 6),
            'timestamp': time.time(),
            'heading': random.randint(0, 359)}

def get_valid_emission_vehicle_id(vehicle_id, version=4):
    if vehicle_id:
        try:
            vehicle_id = str(vehicle_id).lower()
            UUID(vehicle_id, version=version)
            return vehicle_id
        except:
            pass

    raise InvalidUsage('This vehicleId is not valid. Remember to use a UUID.')

def get_valid_emission_vehicle_type(vehicle_type):
    if vehicle_type:
        try:
            vehicle_type = str(vehicle_type).lower()
            if vehicle_type in ['bus', 'taxi', 'tram', 'train']:
                return vehicle_type
        except:
            pass

    raise InvalidUsage('This vehicleType is not valid in Snowdonia. Try bus, taxi, tram or train.')

def get_valid_emission_latitude(latitude):
    if latitude:
        try:
            latitude = round(float(latitude), 6)
            if TOWN_BOUNDAIRES_BOX['south'] <= latitude <= TOWN_BOUNDAIRES_BOX['north']:
                return latitude
        except:
            pass

    message = 'This vehicle latitude is out of Snowdonia limits. Try something between [%s, %s]' % (TOWN_BOUNDAIRES_BOX['south'], TOWN_BOUNDAIRES_BOX['north'])
    raise InvalidUsage(message)

def get_valid_emission_longitude(longitude):
    if longitude:
        try:
            longitude = round(float(longitude), 6)
            if TOWN_BOUNDAIRES_BOX['west'] <= longitude <= TOWN_BOUNDAIRES_BOX['east']:
                return longitude
        except:
            pass

    message = 'This vehicle longitude is out of Snowdonia limits. Try something between [%s, %s]' % (TOWN_BOUNDAIRES_BOX['west'], TOWN_BOUNDAIRES_BOX['east'])
    raise InvalidUsage(message)

def get_valid_emission_timestamp(timestamp):
    if timestamp:
        try:
            timestamp = float(timestamp)
            return timestamp
        except:
            pass

    return time.time()

def get_valid_emission_heading(heading):
    if heading:
        try:
            heading = int(heading)
            if MIN_HEADING <= heading <= MAX_HEADING:
                return heading
        except:
            pass

    message = 'This vehicle heading is not valid. Try something between [%s, %s].' % (MIN_HEADING, MAX_HEADING)
    raise InvalidUsage(message)

def validate_emission_input_data(emission):
    
    if emission:
        data = {}
        if emission.has_key('vehicleId'):
            data['vehicle_id'] = get_valid_emission_vehicle_id(emission['vehicleId'])
        else:
            raise InvalidUsage('vehicleId is an obligatory field.')
    
        if emission.has_key('vehicleType'):
            data['vehicle_type'] = get_valid_emission_vehicle_type(emission['vehicleType'])
        else:
            raise InvalidUsage('vehicleType is an obligatory field.')
    
        if emission.has_key('latitude'):
            data['latitude'] = get_valid_emission_latitude(emission['latitude'])
        else:
            raise InvalidUsage('latitude is an obligatory field.')
    
        if emission.has_key('longitude'):
            data['longitude'] = get_valid_emission_longitude(emission['longitude'])
        else:
            raise InvalidUsage('longitude is an obligatory field.')
    
        if emission.has_key('timestamp'):
            data['timestamp'] = get_valid_emission_timestamp(emission['timestamp'])
        else:
            data['timestamp'] = get_valid_emission_timestamp(None)
    
        if emission.has_key('heading'):
            data['heading'] = get_valid_emission_heading(emission['heading'])
        else:
            raise InvalidUsage('heading is an obligatory field.')
        
        return data

    else:
        raise InvalidUsage('emission can not be a empty body.')

def is_valid_position_emission(latitude, longitude):
    return TOWN_BOUNDAIRES_BOX['south'] <= latitude <= TOWN_BOUNDAIRES_BOX['north'] and TOWN_BOUNDAIRES_BOX['west'] <= longitude <= TOWN_BOUNDAIRES_BOX['east']
    
@app.route(ROOT_PATH, methods=['GET'])
def app_root():
    try:
        with open(README_STATIC_PATH, 'r') as f:
            return Response(markdown(f.read()), mimetype='text/html'), status.HTTP_200_OK
    except:
        return Response('Hello World!', mimetype='text/html'), status.HTTP_200_OK

@app.route(EMISSIONS_PATH, methods=['POST'])
def collect_emissions():
    print request.get_json()
    data = validate_emission_input_data(request.get_json())
    emission = Emission(data['vehicle_id'], data['vehicle_type'],
                        data['latitude'], data['longitude'],
                        data['timestamp'], data['heading'])

    add_emission(emission)
    response = jsonify(emission.generate_output())
    response.status_code = status.HTTP_201_CREATED
    response.headers['location'] = VEHICLES_PATH + str(data['vehicle_id']) +'/'
    return response

@app.route(VEHICLES_PATH + '<uuid:vehicle_id>', methods=['GET'])
def show_emissions_by_vehicle_id(vehicle_id):
    offset = int(request.args.get('offset')) if request.args.get('offset') and int(request.args.get('offset')) >= DEFAULT_OFFSET else DEFAULT_OFFSET
    limit = int(request.args.get('limit')) if request.args.get('limit') and int(request.args.get('limit')) <= DEFAULT_LIMIT else DEFAULT_LIMIT
    total, result = get_emissions_by_vehicle_id(vehicle_id, offset, limit)
    cr = ComplexResponse(total, offset, limit, result)
    response = jsonify(cr.generate_output())
    response.status_code = status.HTTP_200_OK
    return response

@app.route(VEHICLES_TYPE_PATH + '<string:vehicle_type>', methods=['GET'])
def show_emissions_by_vehicle_type(vehicle_type):
    offset = int(request.args.get('offset')) if request.args.get('offset') and int(request.args.get('offset')) >= DEFAULT_OFFSET else DEFAULT_OFFSET
    limit = int(request.args.get('limit')) if request.args.get('limit') and int(request.args.get('limit')) <= DEFAULT_LIMIT else DEFAULT_LIMIT
    total, result = get_emissions_by_vehicle_type(vehicle_type, offset, limit)
    cr = ComplexResponse(total, offset, limit, result)
    response = jsonify(cr.generate_output())
    response.status_code = status.HTTP_200_OK
    return response

@app.route(EMISSIONS_PATH, methods=['GET'])
def show_emissions():
    offset = int(request.args.get('offset')) if request.args.get('offset') and int(request.args.get('offset')) >= DEFAULT_OFFSET else DEFAULT_OFFSET
    limit = int(request.args.get('limit')) if request.args.get('limit') and int(request.args.get('limit')) <= DEFAULT_LIMIT else DEFAULT_LIMIT
    total, result = get_emissions(offset, limit)
    cr = ComplexResponse(total, offset, limit, result)
    response = jsonify(cr.generate_output())
    response.status_code = status.HTTP_200_OK
    return response

""" Error handlers
"""
# @app.errorhandler(404)
# def page_not_found(e):
#    """ By default will redirect any 404 error page to app root.
#    """
#    return redirect(url_for('app_root'))

@app.errorhandler(InvalidUsage)
def handle_invalid_input(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

if __name__ == '__main__':
    host = '127.0.0.1'
    port = int(os.environ.get('PORT', 5000))
    app.run(threaded=True, debug=True, host=host, port=port)
