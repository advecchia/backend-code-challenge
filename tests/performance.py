from locust import HttpLocust, TaskSet, task
import uuid, random, time

ROOT_PATH = '/'
API_VERSION = '1' # Please use simple ordinal there
API_ROOT_PATH = ROOT_PATH + 'api/v' + API_VERSION + '/'
EMISSIONS_PATH = API_ROOT_PATH + 'emissions/'
VEHICLES_PATH = EMISSIONS_PATH + 'vehicles/'
VEHICLES_TYPE_PATH = VEHICLES_PATH + 'type/'

TOWN_CENTRE = {'latitude': 52.902700, 'longitude': -3.812850}
TOWN_BOUNDAIRES_RADIUS = 50000.0 # 50 km in meters
TOWN_BOUNDAIRES_SCALE = TOWN_BOUNDAIRES_RADIUS / 100000 # 0.5 max degree 
TOWN_BOUNDAIRES_BOX = {'north': TOWN_CENTRE['latitude'] + TOWN_BOUNDAIRES_SCALE,
                       'south': TOWN_CENTRE['latitude'] - TOWN_BOUNDAIRES_SCALE,
                       'west': TOWN_CENTRE['longitude'] - TOWN_BOUNDAIRES_SCALE,
                       'east': TOWN_CENTRE['longitude'] + TOWN_BOUNDAIRES_SCALE}
DEFAULT_VEHICLES_IDS = [str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4())]
DEFAULT_VEHICLES_TYPES = ['bus', 'taxi', 'tram', 'train'] 

class ServerTasks(TaskSet):
    def on_start(self):
        self.populate_minimum_emissions()

    def populate_minimum_emissions(self):
        """ Generates first four emissions, one of each vehicle type to be used
        in the tests.
        """
        for i in range(4):
            emission = self.generate_mock_emission()
            emission['vehicleId'] = DEFAULT_VEHICLES_IDS[i]  # obligate all four vehicle ids
            emission['vehicleType'] = DEFAULT_VEHICLES_TYPES[i]  # obligate all four vehicle types
            self.client.post(EMISSIONS_PATH, json=emission)

    def generate_mock_emission(self):
        return {'vehicleId': str(uuid.uuid4()), 
            'vehicleType': random.choice(DEFAULT_VEHICLES_TYPES),
            'latitude':round(random.uniform(TOWN_BOUNDAIRES_BOX['south'], TOWN_BOUNDAIRES_BOX['north']), 6),
            'longitude':round(random.uniform(TOWN_BOUNDAIRES_BOX['west'], TOWN_BOUNDAIRES_BOX['east']), 6),
            'timestamp': time.time(),
            'heading': random.randint(0, 359)}

    @task(1)
    def index(self):
        self.client.get(ROOT_PATH)
        
    @task(16) # accessed 80% of time
    def post_emissions(self):
        self.client.post(EMISSIONS_PATH, json=self.generate_mock_emission())

    @task(1)
    def get_emissions(self):
        self.client.get(EMISSIONS_PATH)

    @task(1)
    def get_emissions_by_vehicle_id(self):
        vehicle_id = random.choice(DEFAULT_VEHICLES_IDS)
        self.client.get(VEHICLES_PATH + vehicle_id)

    @task(1)
    def get_emissions_by_vehicle_type(self):
        vehicle_type = random.choice(DEFAULT_VEHICLES_TYPES)
        self.client.get(VEHICLES_TYPE_PATH + vehicle_type)

class ServerDemand(HttpLocust):
    task_set = ServerTasks
    min_wait = 20000
    max_wait = 20000