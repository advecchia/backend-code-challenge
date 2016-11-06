import os, requests
from flask_api import status
port = int(os.environ.get('PORT', 5000))

class Emitter(object):
    """A class that make communication between simulation and emission API. It
    takes a list of emissions and make a http request. It returns only the number
    of success and fail requests.
    """
    def __init__(self):
        self.url = 'http://0.0.0.0:' + str(port) + '/api/v1/emissions'
        self.emissions = []
    
    def emit(self):
        """Send requests for each emission and returns a tuple containing success
        and fail response numbers.
        """
        success = 0
        fails = 0
        for emission in self.emissions:
            response = requests.post(self.url, json=emission.generate_output())
            if response.status_code == status.HTTP_201_CREATED:
                success += 1
            else:
                fails += 1
                #print response.text # Enable to see response error message

        self.emissions = []
        return (success, fails)       