class ComplexResponse(object):
    """A class that encapsulates information about a request response, this is
    used to make a better end user response, and can be used for pagination.
    """
    def __init__(self, total, offset, limit, data):
        self.total = total
        self.offset = offset
        self.limit = limit
        self.data = data

    def generate_output(self):
        """Generates a dictionary containing informations of response to be
        parsed by a json library.
        """
        output = dict()
        output['total'] = self.total
        output['offset'] = self.offset
        output['limit'] = self.limit
        output['data'] = self.data
        return output

    def __str__(self):
        data = []
        data.append('total='+str(self.total))
        data.append('offset='+str(self.offset))
        data.append('limit='+str(self.limit))
        data.append('data='+str(self.data))
        return '\ComplexResponse: {' + ','.join(data) + '}'