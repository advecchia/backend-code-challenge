import time
from client.position import Position

class Direction(object):
    def __init__(self, position=Position(), timestamp=time.time(), heading=0):
        self.position = position
        self.timestamp = timestamp
        self.heading = heading

    def generate_output(self):
        output = dict()
        output['position'] = self.position.generate_output()
        output['timestamp'] = self.timestamp
        output['heading'] = self.heading
        return output

    def __str__(self):
        data = []
        data.append('position='+str(self.position))
        data.append('timestamp='+str(self.timestamp))
        data.append('heading='+str(self.heading))
        return '\nDirection: {' + ','.join(data) + '}'