import uuid, random
from client.direction import Direction

VEHICLE_TYPES = ['bus', 'taxi', 'tram', 'train']

class Vehicle(object):
    """A class that encapsulates information about a vehicle identification, 
    type, and direction.
    """
    def __init__(self, uuid=uuid.uuid4(), vehicle_type=random.choice(VEHICLE_TYPES), 
                 direction=Direction()):
        self.vehicle_id = str(uuid)
        self.vehicle_type = vehicle_type
        self.direction = direction

    def generate_output(self):
        """Generates a dictionary containing informations of vehicle to be
        parsed by a json library.
        """
        output = dict()
        output['vehicleId'] = self.vehicle_id
        output['vehicleType'] = self.vehicle_type
        output['direction'] = self.direction.generate_output()
        return output

    def __str__(self):
        data = []
        data.append('vehicle_id='+str(self.vehicle_id))
        data.append('vehicle_type='+str(self.vehicle_type))
        data.append('direction='+str(self.direction))
        return '\nVehicle: {' + ','.join(data) + '}'