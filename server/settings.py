""" Keeps a list of constant values that can be used for configuration of server 
and simulation.
"""

import os

##################
# Flask constants
##################
# Usually used host that allows access to server when it is a remote application.
DEFAULT_FLASK_EXTERNAL_HOST = '0.0.0.0'
# If defined, use the system environment Flask port to connect, in other case 
# use a default value.
DEFAULT_FLASK_PORT = int(os.environ.get('PORT', 5000))
# Activates the debug mode for application.
DEFAULT_FLASK_DEBUG_MODE = True

#######################
# City map constraints
#######################
CURRENT_STATIC_PATH = os.path.dirname(os.path.abspath(__file__))
# Hard coded longitude and latitude of Snowdonia Park in UK, this is used as the 
# Town center for simulation and validation.
LONGITUDE = 'longitude'
LATITUDE = 'latitude'
TOWN_CENTER = {LONGITUDE: -3.812850, LATITUDE: 52.902700}
# Max radius (in meters) between town center and his boundaries.
TOWN_BOUNDAIRES_RADIUS = 50000.0 # 50 km in meters
# The length in meters of an arc in the planet earth at Town center latitude.
EARTH_ARC_LENGTH_AT_TOWN_LATITUDE = 111000.0 # 111 km in meters
# The length in meters of an arc in the planet earth at Town center longitude.
EARTH_ARC_LENGTH_AT_TOWN_LONGITUDE = 67000.0 # 67 km in meters
# Using Town radius and we can calculate the max degree variation between center 
# and its boundaries, this is necessary to calculate latitude and longitude for 
# vehicles.
TOWN_MAX_DEGREE_VARIATION = TOWN_BOUNDAIRES_RADIUS / (2 * TOWN_BOUNDAIRES_RADIUS) # 0.5 max degree variation for N-S or W-E
# The real max degree variation in relation to the Town center latitude.
TOWN_LATITUDE_MAX_DEGREE_VARIATION = TOWN_BOUNDAIRES_RADIUS / EARTH_ARC_LENGTH_AT_TOWN_LATITUDE # 0.45 max degree variation for N-S
# The real max degree variation in relation to the Town center longitude.
TOWN_LONGITUDE_MAX_DEGREE_VARIATION = TOWN_BOUNDAIRES_RADIUS / EARTH_ARC_LENGTH_AT_TOWN_LONGITUDE # 0.75 max degree variation for W-E
# The Town center rectangle box containing minimum and maximum latitude and longitude. 
NORTH = 'north'
SOUTH = 'south'
EAST = 'east'
WEST = 'west'
TOWN_BOUNDAIRES_BOX = {NORTH: TOWN_CENTER[LATITUDE] + TOWN_MAX_DEGREE_VARIATION,
                       SOUTH: TOWN_CENTER[LATITUDE] - TOWN_MAX_DEGREE_VARIATION,
                       EAST: TOWN_CENTER[LONGITUDE] + TOWN_MAX_DEGREE_VARIATION,
                       WEST: TOWN_CENTER[LONGITUDE] - TOWN_MAX_DEGREE_VARIATION}
# Minimum and maximum acceptable values for vehicle heading (360 degree angle of its direction).
MIN_HEADING = 0
MAX_HEADING = 359
# Default values of offset and limit for pagination that can be used in request calls.
DEFAULT_OFFSET = 0
DEFAULT_LIMIT = 250
# A list containing all valid vehicle types.
VALID_VEHICLE_TYPES = ['bus', 'taxi', 'tram', 'train']
# Maximum values for latitude and longitude range
MAX_LATITUDE = 90.0
MIN_LATITUDE = -90.0
MAX_LONGITUDE = 180.0
MIN_LONGITUDE = -180.0

#####################
# Database Constants
#####################
# Location of current database of Snowdonia.
DATABASE_PATH = CURRENT_STATIC_PATH + '/../db/snowdonia.db'
# Location of creation schema for Snowdonia database.
DATABASE_SCHEMA_PATH = CURRENT_STATIC_PATH + '/../db/schema.sql'

################
# API Constants
################
# Site root.
ROOT_PATH = '/'
# API version definition.
API_VERSION = '1' # Please use simple ordinal there.
API_ROOT_PATH = ROOT_PATH + 'api/v' + API_VERSION + '/'
# Manipulate emissions.
EMISSIONS_PATH = API_ROOT_PATH + 'emissions/'
# Manipulate emission vehicles using vehicle identifier.
VEHICLES_PATH = EMISSIONS_PATH + 'vehicles/'
# Manipulate emission vehicles by vehicle type.
VEHICLES_TYPE_PATH = VEHICLES_PATH + 'type/'
# Path of project readme that is used as root view.
README_STATIC_PATH = CURRENT_STATIC_PATH + '/../README.md'
