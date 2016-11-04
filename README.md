# Snowdonia challenge
For information about the challenge, see [CHALLENGE](https://github.com/advecchia/backend-code-challenge/blob/master/CHALLENGE.md) documentation.  
Below you can see information about how to setup your development environment and also how to deploy this code to [Heroku](https://www.heroku.com/). For traffic simulation I used [SUMO](http://sumo.dlr.de/userdoc/index.html) and [JOSM](https://josm.openstreetmap.de/), there is also a how to make your own simulation. For performance I chose [LOCUST](http://locust.io/).  

## Development environment and Heroku deploy  
All development has been done on Ubuntu 14.04 LTS, so I will assume that if you use another version or other OS some changes will be need at your account and risk.  

You need to install some packages, follow the links for instructions:  
[Python](https://www.python.org/downloads/), [LOCUST](http://docs.locust.io/en/latest/installation.html), [Sqlite3](https://www.digitalocean.com/community/tutorials/how-and-when-to-use-sqlite), [SUMO](http://sumo.dlr.de/wiki/Installing), [JOSM](https://josm.openstreetmap.de/wiki/Download).  

Create an account at Heroku website.  

Export the PORT variable to be compatible with Heroku environment. This port is used by gunicorn and flask.  
$ export PORT=5000  

Install Heroku CLI to access Heroku from shell:  
$ wget -O- https://toolbelt.heroku.com/install-ubuntu.sh | sh  

Login to Heroku  
$ heroku login  

Following the below four steps you will be running a local version of Heroku with the code that can be deployed after in another dyno.  

$ git clone https://github.com/advecchia/backend-code-challenge.git  
$ cd backend-code-challenge  
$ pip install -r requirements.txt  
$ heroku local  

Create a remote app on Heroku  
$ heroku create  

Push the master branch to server. By default Heroku deploy will occur with master branch. If you want to change this behavior, read Heroku documentation and change push branch value.  
$ git push heroku master  

Set concurrency configuration to improve performance  
$ heroku config:set WEB_CONCURRENCY=3  

Define the number of instances  
$ heroku ps:scale web=1  

Open the app in the browser  
$ heroku open  

Currently you can access my instance at: [Go to App](http://guarded-plateau-54331.herokuapp.com/).  

## Performance Tests  
A set of performance tests are performed with [LOCUST](http://locust.io/). See this [README](https://github.com/advecchia/backend-code-challenge/blob/master/docs/performance/README.md) documentation for results.  

To run locally use (after setup your environment):  
$ locust -f backend-code-challenge/tests/performance.py --host=http://0.0.0.0:5000  

To run over my deployed instance use the below command:  
$ locust -f backend-code-challenge/tests/performance.py --host=http://guarded-plateau-54331.herokuapp.com  

You now can access a web interface to execute the performance test, there you can add manually two parameters, the max number of concurrent users and the user spawn per second. Access http://127.0.0.1:8089/ in the browser of your preference and enjoy!  
 
## Traffic Simulation  
First of all is necessary to define a map for simulation, this can be done using [JOSM](https://josm.openstreetmap.de/). Open the application and click File > Download from OSM... After grab an area of the map that you want and download as a new layer.  

After this step you will need to remove nodes and edges (delete) that are off of the bounding box of the generated map, this is necessary because they can break the SUMO simulation. Another thing to do is simplify ways (Shift + y) this will remove some nodes from the map and improve performance simulation.  

### Generating Network  
As a simulation option I choose to construct a scaled map from Snowdonia (toy grid map) at about 5% scale, this will allow a much better simulation experience. Inside the emitter code I make the expected corrections to Town lat/long coordinates and heading to deal with challenge specifications.  

Executing the below command will generate the experiment network (see figure).  
$ netgenerate -g --grid.number 21 --grid.length 250 --o snowdonia.grid.net.xml --tls.guess --tls.join --default.lanenumber 2 --no-turnarounds --no-turnarounds.tls --no-left-connections  

![Grid network](https://github.com/advecchia/backend-code-challenge/blob/master/sumo/grid_network.png "Grid network")  

This network provide a simulated city with about 5 kilometers in both directions, roads of 250 meters with two lanes in both sides and traffic lights system. The vehicle velocity is about 50 km/h.  

### Generating Traffic  
**Creating some TAZ (Traffic Assignment Zone)**  
A TAZ is an area of network edges that are used for source and destination of vehicle trips. See this documentation [Describing TAZ](http://sumo.dlr.de/wiki/Demand/Importing_O/D_Matrices#Describing_the_TAZ) it describe how to develop your own TAZ file.  

This is some a time consuming task because it is needed to search in the network file (or visualize them with sumo-gui) each edge that you want to put in some zone. See the resulting [TAZ file](https://github.com/advecchia/backend-code-challenge/blob/master/sumo/snowdonia.taz.xml).  

**Creating OD (Origin/Destination) Matrix**  
Origin/Destination matrix are files that describe the vehicle demand and flow time used for generate vehicle routes.
See this documentation [Describing V Format](http://sumo.dlr.de/wiki/Demand/Importing_O/D_Matrices#The_V_format). See the resulting matrices for [taxi](https://github.com/advecchia/backend-code-challenge/blob/master/sumo/taxi.od.matrix), [bus](https://github.com/advecchia/backend-code-challenge/blob/master/sumo/bus.od.matrix), [tram](https://github.com/advecchia/backend-code-challenge/blob/master/sumo/tram.od.matrix) and [train](https://github.com/advecchia/backend-code-challenge/blob/master/sumo/train.od.matrix).  

**Creating Trips and Flows for OD**  
This step translates the demand matrices in a flow type file that describe the flow of vehicles in some region of the network and also in a trip file that describe the trip for each vehicle type from point to point. See this documentation about [Flow and Trip](http://sumo.dlr.de/wiki/Demand/Shortest_or_Optimal_Path_Routing) definitions.  
$ od2trips -n snowdonia.taz.xml --od-matrix-files taxi.od.matrix,bus.od.matrix,tram.od.matrix,train.od.matrix -o snowdonia.trips.xml --flow-output snowdonia.flow.xml --save-configuration snowdonia.od2trips.config.xml  
$ od2trips -c snowdonia.od2trips.config.xml  

See an example of a trip:  
> <trip id="471" depart="7192.36" from="10/9to10/10" to="0/1to0/0" type="taxi" fromTaz="taxi_center_and_NW" toTaz="taxi_center_and_SW" departLane="free" departSpeed="max"/>  

See an example of a flow:  
> <flow id="26" begin="0.00" end="7200.00" number="10" type="tram" fromTaz="tram_center_and_SSE" toTaz="tram_center_and_NNW" departLane="free" departSpeed="max"/>  

**Creating Routes**  
This step will convert each vehicle trip definition in a Shortest Path route for each vehicle. This step may take some time.  
$ duarouter --trip-files snowdonia.trips.xml --net-file snowdonia.grid.net.xml --output-file snowdonia.rou.xml --taz-files snowdonia.taz.xml,snowdonia.vehicles.add.xml --with-taz --save-configuration snowdonia.duarouter.config.xml  
$ duarouter -c snowdonia.duarouter.config.xml  

See an example of a vehicle route, the route edges list define each edge that the vehicle need to pass to accomplish its trip:  
> <vehicle id="771" type="taxi" depart="505.14" departLane="free" departSpeed="max" fromTaz="taxi_NW" toTaz="taxi_SW"><route edges="0/19to1/19 1/19to1/18 1/18to1/17 1/17to1/16 1/16to1/15 1/15to1/14 1/14to1/13 1/13to1/12 1/12to1/11 1/11to1/10 1/10to1/9 1/9to1/8 1/8to1/7 1/7to1/6 1/6to1/5 1/5to1/4 1/4to1/3 1/3to1/2 1/2to1/1 1/1to0/1"/></vehicle>  

**Creating Simulation configuration file**  
This step create the configuration file that will be used when running the sumo simulation, it uses the grid network of Snowdonia and the routing file.  
$ sumo --save-configuration snowdonia.sumo.cfg -n snowdonia.grid.net.xml -r snowdonia.rou.xml  

### Run SUMO - Simulation For Urban Mobility  
You can run the simulation in two way, first in the console, the simulation run in a few seconds. Another way is running the sumo-gui interface, there you can visualize the vehicle trips inside the network and also can change some behavior of this view, like delay of step simulation and color of occupancy edges.  

Run on console:  
$ sumo -c snowdonia.sumo.cfg  

Run on GUI interface:  
$ sumo-gui -c snowdonia.sumo.cfg  

### Runnig the vehicle emitter using SUMO Traci Interface and Python
To accomplish the task and make the vehicle GPS emitting in the Snowdonia network I need to use [Traci Interface](http://www.sumo.dlr.de/wiki/TraCI/Interfacing_TraCI_from_Python).