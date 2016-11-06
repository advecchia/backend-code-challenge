import os, sys, argparse, subprocess, uuid
from collections import defaultdict
from time import time

sys.path.append(os.path.join(os.getcwd(),os.path.dirname(__file__), '../'))
from server import settings as s
from server.emitter import Emitter
from client.vehicle import Vehicle
from client.direction import Direction
from client.position import Position
from client.emission import Emission 

#
# Simulation configuration options
#
PORT = "--port"
MIN_PORT = "-p"
DEFAULT_PORT = 8813
MAP_SCALE = 0.05
DEVICE_TIME_TO_EMIT = 20.0

# Correcting sumo path environment
if 'SUMO_HOME' not in os.environ:
    os.environ['SUMO_HOME'] = '/usr/share/sumo/'
    sys.path.append('/usr/share/sumo/')

tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
sys.path.append(tools)
import traci

# Initialize a instance of sumo with the configuration, this allow to traci to communicate
# and access vehicles information
sumo_process = subprocess.Popen(['sumo', '-c', 'map/snowdonia.sumo.cfg', '--remote-port', '8813'])

def parse():
    """Read the input and put the words in a dictionary.
    """

    parser = argparse.ArgumentParser(description="Execute an simple algorithm for swarm intelligence.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    # Simulation configuration group
    groupSim = parser.add_argument_group("Simulation group","The parameters that define the basics of simulation execution.")
    groupSim.add_argument(MIN_PORT, PORT, dest=PORT, nargs=1, metavar="number", default=DEFAULT_PORT, help="Flag to inform the port to communicate with traci-hub or SUMO.")

    args = parser.parse_args()
    params = vars(args)

    #"""
    # Removes the parameter not inserted in the input
    for key,value in params.items():
        if value is None:
            del params[key]
        elif not isinstance(value, list):
            params[key] = []
            params[key].append(value)
    #"""
    return params

def get_vehicle_mapping_coordinates(x, y):
    """Generates the longitude and latitude of a vehicle based in the simulated
    network re-scale and decimal distance to a degree conversion, this is only a 
    gross conversion.
    """
    scale_x = x / MAP_SCALE
    scale_y = y / MAP_SCALE

    longitude = s.TOWN_CENTER['longitude']
    scale_x_degree = scale_y / s.EARTH_ARC_LENGTH_AT_TOWN_LONGITUDE
    if scale_x <= s.TOWN_BOUNDAIRES_RADIUS: # radius is at same time center point of the flattened city
        longitude -= s.TOWN_LONGITUDE_MAX_DEGREE_VARIATION - scale_x_degree
    else:
        longitude += scale_x_degree - s.TOWN_LONGITUDE_MAX_DEGREE_VARIATION

    latitude = s.TOWN_CENTER['latitude']
    scale_y_degree = scale_y / s.EARTH_ARC_LENGTH_AT_TOWN_LATITUDE
    if scale_y <= s.TOWN_BOUNDAIRES_RADIUS: # radius is at same time center point of the flattened city
        latitude -= s.TOWN_LATITUDE_MAX_DEGREE_VARIATION - scale_y_degree
    else:
        latitude += scale_y_degree - s.TOWN_LATITUDE_MAX_DEGREE_VARIATION
    
    #print '(x=%f, y=%f) -> (longitude=%f, latitude=%f)' % (x, y, longitude, latitude)
    return (longitude, latitude)

def main():
    # Parse the input command.
    params = parse()

    # For the use of SUMO with traci-hub.
    port = int(params[PORT].pop()) 
    if port >= 0:
        traci.init(port)
    else:
        traci.init(DEFAULT_PORT)

    # For stop execution
    total_departed = 0
    total_arrived = 0
    
    # For time execution calculation
    time_total = 0
    
    # For each iteration of the simulation.
    time_step = 1

    vehicles_emitters = defaultdict(dict) # {vehicle_id: [time, vehicle]}
    to_emit_id_list = []
    emitter = Emitter()

    while True:

        # Double of end flow time.
        if time_step > 14400:
            traci.close()
            print "\nMessage: traci closed for double time limit."
            break

        # All vehicles have arrived after the flow beginning.
        if time_step > 7200 and total_arrived == total_departed:
            traci.close()
            print "\nMessage: traci normally closed."
            break

        try:
            start_time = time()
            
            #Executes one step
            traci.simulationStep()

            runnig_vehicles_ids = traci.vehicle.getIDList()
            if runnig_vehicles_ids:
                for vehicle_id in runnig_vehicles_ids:
                    longitude, latitude = get_vehicle_mapping_coordinates(traci.vehicle.getPosition(vehicle_id)[0], traci.vehicle.getPosition(vehicle_id)[1])
                    heading = traci.vehicle.getAngle(vehicle_id)
                    position = Position(longitude, latitude)
                    direction = Direction(position, start_time, heading)
                    if vehicle_id not in vehicles_emitters:
                        vehicle_type = traci.vehicle.getTypeID(vehicle_id) # Do not change between simulation steps
                        vehicle = Vehicle(uuid.uuid4(), vehicle_type, direction)
                        vehicles_emitters[vehicle_id] = [0.0, vehicle] # initialize vehicle
                    else: #increment time and update vehicle direction
                        vehicles_emitters[vehicle_id][0] += time() - start_time
                        vehicles_emitters[vehicle_id][1].direction = direction

                    if vehicles_emitters[vehicle_id][0] >= DEVICE_TIME_TO_EMIT: # Time to emit
                        to_emit_id_list.append(vehicle_id)
                        vehicles_emitters[vehicle_id][0] = 0.0 # reinitialize the time to emit

            # Sent a batch of emissions requests to server
            emission_message = ''
            if to_emit_id_list:
                emissions = []
                for vehicle_id in to_emit_id_list:
                    vehicle = vehicles_emitters[vehicle_id][1]
                    emission = Emission(vehicle.vehicle_id, 
                                        vehicle.vehicle_type, 
                                        vehicle.direction.position.latitude, 
                                        vehicle.direction.position.longitude, 
                                        vehicle.direction.timestamp, 
                                        vehicle.direction.heading)
                    emissions.append(emission)
                emitter.emissions = emissions
                emission_message += ' Vehicles emitting now (#%d),' % (len(emissions))
                success, fails = emitter.emit()
                emission_message += ' with success=#%d, with fail=#%d.' % (success, fails)
                to_emit_id_list = []

            # Clear the list of emitter from arrived vehicles
            arrived_vehicles_ids = traci.simulation.getArrivedIDList()
            for vehicle_id in arrived_vehicles_ids:
                vehicles_emitters.pop(vehicle_id, None)

            time_step += 1
            time_diff = time() - start_time
            time_total += time_diff
            output_message = "\rTimestep #%d took %5.3f ms. Total time %5.3f ms. Running Vehicles %d." % (time_step, time_diff, time_total, len(runnig_vehicles_ids))
            output_message += emission_message
            sys.stdout.write(output_message)
            sys.stdout.flush()

        except traci.FatalTraCIError as message:
            print "\nMessage:", message
            traci.close()
            break

    exit()

if __name__ == '__main__':
    main()