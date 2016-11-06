from uuid import UUID
from client.errorhandlers import InvalidUsage
import settings as s
import time
from flask import request

class EmissionValidator(object):
    """ This class encapsulate methods used to valid payload input for an emission.
    If everything is correct it generates a dictionary containing all correct 
    emission data.  
    """
    def __init__(self):
        pass

    def get_valid_emission_vehicle_id(self, vehicle_id, version=4):
        """ Validates if a input vehicle id is UUID format string.
        """
        if vehicle_id:
            try:
                vehicle_id = str(vehicle_id).lower()
                UUID(vehicle_id, version=version)
                return vehicle_id
            except:
                pass
    
        raise InvalidUsage('This vehicleId is not valid. Remember to use a UUID.')
    
    def get_valid_emission_vehicle_type(self, vehicle_type):
        """ Validates if a input vehicle type is valid. Uses a hard coded defined 
        list of valid vehicle types.
        """
        if vehicle_type:
            try:
                vehicle_type = str(vehicle_type).lower()
                if vehicle_type in s.VALID_VEHICLE_TYPES:
                    return vehicle_type
            except:
                pass
    
        raise InvalidUsage('This vehicleType is not valid in Snowdonia. Try ' + ', '.join(str(vt) for vt in s.VALID_VEHICLE_TYPES) + '.')
    
    def get_valid_emission_latitude(self, latitude):
        """ Validates if a input vehicle latitude is valid. Uses constant values to 
        do the job.
        """
        if latitude or (s.MIN_LATITUDE <= round(float(latitude), 6) <= s.MAX_LATITUDE):
            try:
                latitude = round(float(latitude), 6)
                if s.TOWN_BOUNDAIRES_BOX['south'] <= latitude <= s.TOWN_BOUNDAIRES_BOX['north']:
                    return latitude
            except:
                pass
    
        message = 'This vehicle latitude is out of Snowdonia limits. Try something between [%s, %s]' % (s.TOWN_BOUNDAIRES_BOX['south'], s.TOWN_BOUNDAIRES_BOX['north'])
        raise InvalidUsage(message)
    
    def get_valid_emission_longitude(self, longitude):
        """ Validates if a input vehicle longitude is valid. Uses constant values to 
        do the job.
        """
        if longitude or (s.MIN_LONGITUDE <= round(float(longitude), 6) <= s.MAX_LONGITUDE):
            try:
                longitude = round(float(longitude), 6)
                if s.TOWN_BOUNDAIRES_BOX['west'] <= longitude <= s.TOWN_BOUNDAIRES_BOX['east']:
                    return longitude
            except:
                pass
    
        message = 'This vehicle longitude is out of Snowdonia limits. Try something between [%s, %s]' % (s.TOWN_BOUNDAIRES_BOX['west'], s.TOWN_BOUNDAIRES_BOX['east'])
        raise InvalidUsage(message)
    
    def get_valid_emission_timestamp(self, timestamp):
        """ Validates if a input vehicle timestamp is valid. If not, generates a 
        correct one.
        """
        if timestamp:
            try:
                timestamp = float(timestamp)
                return timestamp
            except:
                pass
    
        return time.time()
    
    def get_valid_emission_heading(self, heading):
        """ Validates if a input vehicle heading is valid. Uses constant values to 
        do the job.
        """
        if heading or int(float(heading)) >= 0:
            try:
                heading = int(float(heading))
                if s.MIN_HEADING <= heading <= s.MAX_HEADING:
                    return heading
            except:
                pass
    
        message = 'This vehicle heading is not valid. Try something between [%s, %s].' % (s.MIN_HEADING, s.MAX_HEADING)
        raise InvalidUsage(message)
    
    def validate_emission_input_data(self, emission):
        """ Takes one emission dictionary and validate each of vehicle input data.
        """
        if emission:
            data = {}
            if emission.has_key('vehicleId'):
                data['vehicle_id'] = self.get_valid_emission_vehicle_id(emission['vehicleId'])
            else:
                raise InvalidUsage('vehicleId is an obligatory field.')
        
            if emission.has_key('vehicleType'):
                data['vehicle_type'] = self.get_valid_emission_vehicle_type(emission['vehicleType'])
            else:
                raise InvalidUsage('vehicleType is an obligatory field.')
        
            if emission.has_key('latitude'):
                data['latitude'] = self.get_valid_emission_latitude(emission['latitude'])
            else:
                raise InvalidUsage('latitude is an obligatory field.')
        
            if emission.has_key('longitude'):
                data['longitude'] = self.get_valid_emission_longitude(emission['longitude'])
            else:
                raise InvalidUsage('longitude is an obligatory field.')
        
            if emission.has_key('timestamp'):
                data['timestamp'] = self.get_valid_emission_timestamp(emission['timestamp'])
            else:
                data['timestamp'] = self.get_valid_emission_timestamp(None)
        
            if emission.has_key('heading'):
                data['heading'] = self.get_valid_emission_heading(emission['heading'])
            else:
                raise InvalidUsage('heading is an obligatory field.')
            
            return data
    
        else:
            raise InvalidUsage('emission can not be a empty body.')

class QueryParameterValidator(object):
    def __init__(self):
        pass

    def validate_query_parameters(self, request):
        """ Validates request parameters (offset and limit) and a if they are 
        absence assign default values.
        """
        offset = int(request.args.get('offset')) if request and request.args and request.args.get('offset') and int(request.args.get('offset')) >= s.DEFAULT_OFFSET else s.DEFAULT_OFFSET
        limit = int(request.args.get('limit')) if request and request.args and request.args.get('limit') and int(request.args.get('limit')) <= s.DEFAULT_LIMIT else s.DEFAULT_LIMIT
        return [offset, limit]