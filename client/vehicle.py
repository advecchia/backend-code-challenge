import uuid, random
from client.direction import Direction

VEHICLE_TYPES = ['bus', 'taxi', 'tram', 'train']

class Vehicle(object):
    def __init__(self, uuid=uuid.uuid4(), vehicle_type=random.choice(VEHICLE_TYPES), 
                 direction=Direction()):
        self.vechicle_id = str(uuid)
        self.vehicle_type = vehicle_type
        self.direction = direction

    def generate_output(self):
        output = dict()
        output['vechicleId'] = self.vechicle_id
        output['vehicleType'] = self.vehicle_type
        output['direction'] = self.direction.generate_output()
        return output

    def __str__(self):
        data = []
        data.append('vechicle_id='+str(self.vechicle_id))
        data.append('vehicle_type='+str(self.vehicle_type))
        data.append('direction='+str(self.direction))
        return '\nVehicle: {' + ','.join(data) + '}'