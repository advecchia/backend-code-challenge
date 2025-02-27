import uuid, random, time

VEHICLE_TYPES = ['bus', 'taxi', 'tram', 'train']

class Emission(object):
    """A class that encapsulates information about a vehicle GPS emission.
    """
    def __init__(self, uuid=uuid.uuid4(), vehicle_type=random.choice(VEHICLE_TYPES), 
                 latitude=0, longitude=0, timestamp=time.time(), heading=0):
        self.vehicle_id = str(uuid)
        self.vehicle_type = vehicle_type
        self.latitude = latitude
        self.longitude = longitude
        self.timestamp = timestamp
        self.heading = heading

    def generate_output(self):
        """Generates a dictionary containing informations of emission to be
        parsed by a json library.
        """
        output = dict()
        output['vehicleId'] = self.vehicle_id
        output['vehicleType'] = self.vehicle_type
        output['latitude'] = self.latitude
        output['longitude'] = self.longitude
        output['timestamp'] = self.timestamp
        output['heading'] = self.heading
        return output

    def __str__(self):
        data = []
        data.append('vehicle_id='+str(self.vehicle_id))
        data.append('vehicle_type='+str(self.vehicle_type))
        data.append('latitude='+str(self.latitude))
        data.append('longitude='+str(self.longitude))
        data.append('timestamp='+str(self.timestamp))
        data.append('heading='+str(self.heading))
        return '\nEmission: {' + ','.join(data) + '}'