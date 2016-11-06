class Position(object):
    """A class that encapsulates information about a vehicle latitude and 
    longitude positions.
    """
    def __init__(self, longitude=0, latitude=0):
        self.longitude = longitude
        self.latitude = latitude

    def generate_output(self):
        """Generates a dictionary containing informations of position to be
        parsed by a json library.
        """
        output = dict()
        output['longitude'] = self.longitude
        output['latitude'] = self.latitude
        return output

    def __str__(self):
        data = []
        data.append('longitude='+str(self.longitude))
        data.append('latitude='+str(self.latitude))
        return '\nPosition: {' + ','.join(data) + '}'