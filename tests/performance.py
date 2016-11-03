from locust import HttpLocust, TaskSet, task
import uuid, random, time, sys, os
sys.path.append(os.path.join(os.getcwd(),os.path.dirname(__file__), '../'))
from server import settings as s

DEFAULT_VEHICLES_IDS = [str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4())] 

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
            emission['vehicleType'] = s.VALID_VEHICLE_TYPES[i]  # obligate all four vehicle types
            self.client.post(s.EMISSIONS_PATH, json=emission)

    def generate_mock_emission(self):
        return {'vehicleId': str(uuid.uuid4()), 
            'vehicleType': random.choice(s.VALID_VEHICLE_TYPES),
            'latitude':round(random.uniform(s.TOWN_BOUNDAIRES_BOX['south'], s.TOWN_BOUNDAIRES_BOX['north']), 6),
            'longitude':round(random.uniform(s.TOWN_BOUNDAIRES_BOX['west'], s.TOWN_BOUNDAIRES_BOX['east']), 6),
            'timestamp': time.time(),
            'heading': random.randint(s.MIN_HEADING, s.MAX_HEADING)}

    @task(1)
    def index(self):
        self.client.get(s.ROOT_PATH)
        
    @task(16) # accessed 80% of time
    def post_emissions(self):
        self.client.post(s.EMISSIONS_PATH, json=self.generate_mock_emission())

    @task(1)
    def get_emissions(self):
        self.client.get(s.EMISSIONS_PATH)

    @task(1)
    def get_emissions_by_vehicle_id(self):
        vehicle_id = random.choice(DEFAULT_VEHICLES_IDS)
        self.client.get(s.VEHICLES_PATH + vehicle_id)

    @task(1)
    def get_emissions_by_vehicle_type(self):
        vehicle_type = random.choice(s.VALID_VEHICLE_TYPES)
        self.client.get(s.VEHICLES_TYPE_PATH + vehicle_type)

class ServerDemand(HttpLocust):
    task_set = ServerTasks
    min_wait = 20000
    max_wait = 20000