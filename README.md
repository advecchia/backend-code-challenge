# Snowdonia challenge
For information about the challenge, see [CHALLENGE](https://github.com/advecchia/backend-code-challenge/blob/master/CHALLENGE.md) documentation.

See below the instructions for setup a experiment, run and visualize the simulation results.
TBD.

## SUMO - Simulation For Urban Mobility
netconvert --type-files osmNetconvert.typ.xml --osm-files snowdonia.osm.xml --output-file snowdonia.net.xml --remove-edges.isolated --roundabouts.guess --ramps.guess

### Environment configuration
 
### Generating Network

### Generating Traffic and trips

### Run simulation

### Performance Tests
locust -f performance.py --host=http://127.0.0.1:5000
