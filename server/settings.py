import os

#######################
# City map constraints
#######################
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
VALID_VEHICLE_TYPES = ['bus', 'taxi', 'tram', 'train']

#####################
# Database Constants
#####################
DATABASE_PATH = CURRENT_STATIC_PATH + '/../db/snowdonia.db'
DATABASE_SCHEMA_PATH = CURRENT_STATIC_PATH + '/../db/schema.sql'

################
# API Constants
################
ROOT_PATH = '/'
API_VERSION = '1' # Please use simple ordinal there
API_ROOT_PATH = ROOT_PATH + 'api/v' + API_VERSION + '/'
EMISSIONS_PATH = API_ROOT_PATH + 'emissions/'
VEHICLES_PATH = EMISSIONS_PATH + 'vehicles/'
VEHICLES_TYPE_PATH = VEHICLES_PATH + 'type/'
README_STATIC_PATH = CURRENT_STATIC_PATH + '/../README.md'
