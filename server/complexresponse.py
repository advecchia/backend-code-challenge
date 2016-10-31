class ComplexResponse(object):
    def __init__(self, total, offset, limit, data):
        self.total = total
        self.offset = offset
        self.limit = limit
        self.data = data

    def generate_output(self):
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