class Position(object):
    def __init__(self, latitude=0, longitude=0):
        self.latitude = latitude
        self.longitude = longitude

    def generate_output(self):
        output = dict()
        output['latitude'] = self.latitude
        output['longitude'] = self.longitude
        return output

    def __str__(self):
        data = []
        data.append('latitude='+str(self.latitude))
        data.append('longitude='+str(self.longitude))
        return '\nPosition: {' + ','.join(data) + '}'