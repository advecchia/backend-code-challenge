# SUMO Simulation Description
SUMO is a microscopic traffic simulation framework. It had been developed in C++ and offer some plugins that allows communication with its environment, I used Traci plugin for Python. This plugin can be used to access information of network, traffic signal and vehicles and also its manipulation. Below I described how to create your own toy network and execute an experiment.  

### <a id="toc"></a>Table of Contents 
 * [Go back to home](https://github.com/advecchia/backend-code-challenge/blob/master/README.md)  
 * [Traffic Simulation](#traffic-simulation)  
 * [Generating Network](#generating-network)  
 * [Generating Traffic](#generating-traffic)  
 * [Run SUMO](#run-sumo)  
 * [Runnig the vehicle emitter](#running-experiment)  

## Traffic Simulation <a id="traffic-simulation"></a> [^](#toc "To top")  
First of all we need to define a map for simulation, this can be done using [JOSM](https://josm.openstreetmap.de/). Open the application and click File > Download from OSM... After grab an area of the map that you want and download as a new layer.  

After this step you will need to remove nodes and edges (delete) that are off of the bounding box of the generated map, this is necessary because they can break the SUMO simulation. Another thing to do is simplify ways (Shift + y) this will remove some nodes from the map and improve performance simulation.  

I tried  this approach first and ended with a map network with about 200MB, for the sake of this experiment it is a realistic one but not practical for my own computer. See below information of that region in OpenStreetMap, a picture of it and its bounding box.

[Snowdonia at OpenStreetMap](https://www.openstreetmap.org/export#map=9/52.8915/-3.6818 "Snowdonia National Park")  
![Snowdonia Map](https://raw.githubusercontent.com/advecchia/backend-code-challenge/master/sumo/map/snowdonia_park.png "Snowdonia Map")  
![Snowdonia Bounding Box](https://raw.githubusercontent.com/advecchia/backend-code-challenge/master/sumo/map/snowdonia_bounding_box.png "Snowdonia Bounding Box")  

With this problem in mind I have to try another way, so I developed a scaled toy map for that region. See it in the next chapter.

### Generating Network <a id="generating-network"></a> [^](#toc "To top")  
As a simulation option I choose to construct a scaled map from Snowdonia (a toy grid map) at about 5% scale, this will allow a much better simulation experience. (Inside the emitter code I make the expected corrections to Town latitude and longitude coordinates to deal with challenge specifications.).  

Executing the below command will generate the experiment network (see figure).  
$ netgenerate -g --grid.number 21 --grid.length 250 --o snowdonia.grid.net.xml --tls.guess --tls.join --default.lanenumber 2 --no-turnarounds --no-turnarounds.tls --no-left-connections  

![Grid network](https://raw.githubusercontent.com/advecchia/backend-code-challenge/master/sumo/map/grid_network.png "Grid network")  

This network provide a simulated city with about 5 kilometers in both directions of the grid, roads of 250 meters with two lanes in both sides and traffic lights system. This is equivalent of about 840 km of traffic area. The vehicle velocity is about 50 km/h.  

Well this network has not the 100 kilometers area of Snowdonia, because of that, at emitter script I make a re-scale that transform the 5 km to 100 km and map the vehicle position (Cartesian coordinates) to longitude and latitude using Earth values of arc distance at the Snowdonia Park (real region), very trick but it is a good approximation (for the sake of an experiment). Real Town Centre constants are {LONGITUDE: -3.812850, LATITUDE: 52.902700}.  

### Generating Traffic <a id="generating-traffic"></a> [^](#toc "To top")  
After generating the network, I need to develop some traffic demand, for this I make use of TAZ areas.
A TAZ is an area of network edges that are used for source and destination of vehicle trips. See this documentation [Describing TAZ](http://sumo.dlr.de/wiki/Demand/Importing_O/D_Matrices#Describing_the_TAZ) it describe how to develop your own TAZ file based in a first created network.  

**Creating some TAZ (Traffic Assignment Zone)**  
This is a time consuming task because it is needed to search in the network file (or visualize them with sumo-gui) for each edge that you want to put in some zone. See the resulting [TAZ file](https://github.com/advecchia/backend-code-challenge/blob/master/sumo/map/snowdonia.taz.xml). I mapped the TAZ's areas in a picture to make easy to know where the vehicles will be circulating.  

![Taz and Demand](https://raw.githubusercontent.com/advecchia/backend-code-challenge/master/sumo/map/taz_and_demand.png "Taz and Demand")  

**Creating OD (Origin/Destination) Matrix**  
Origin/Destination matrix are files that describe the vehicle demand and flow time and are used by SUMO for generate vehicle routes. See this documentation [Describing V Format](http://sumo.dlr.de/wiki/Demand/Importing_O/D_Matrices#The_V_format) to know a litte more.  

You can see there the resulting matrices for [taxi](https://github.com/advecchia/backend-code-challenge/blob/master/sumo/map/taxi.od.matrix), [bus](https://github.com/advecchia/backend-code-challenge/blob/master/sumo/map/bus.od.matrix), [tram](https://github.com/advecchia/backend-code-challenge/blob/master/sumo/map/tram.od.matrix) and [train](https://github.com/advecchia/backend-code-challenge/blob/master/sumo/map/train.od.matrix).  

All matrices describe the vehicle flow for each type of vehicle. Each vehicle will arise at one of its TAZ spot (or at center) as marked in the "Taz and Demand" picture and will drive to another of its spots (or to center), vehicles will not drive to the same TAZ that they had arose.  

The next step is create the trips and flows.  

**Creating Trips and Flows for OD**  
This step translates the demand matrices in a flow type file that describe the flow of vehicles types in some region of the network and also in a trip file that describe the trip for each vehicle type from point to point. Both files describe somewhat the same thing but in different form. See this documentation about [Flows and Trips](http://sumo.dlr.de/wiki/Demand/Shortest_or_Optimal_Path_Routing) definition. To do the job, execute the below lines, first create a configuration file and them executes it. 
$ od2trips -n snowdonia.taz.xml --od-matrix-files taxi.od.matrix,bus.od.matrix,tram.od.matrix,train.od.matrix -o snowdonia.trips.xml --flow-output snowdonia.flow.xml --save-configuration snowdonia.od2trips.config.xml  
$ od2trips -c snowdonia.od2trips.config.xml  

There you can see an example of a trip line:  
> <trip id="471" depart="7192.36" from="10/9to10/10" to="0/1to0/0" type="taxi" fromTaz="taxi_center_and_NW" toTaz="taxi_center_and_SW" departLane="free" departSpeed="max"/>  

There you can see an example of a flow line:  
> <flow id="26" begin="0.00" end="7200.00" number="10" type="tram" fromTaz="tram_center_and_SSE" toTaz="tram_center_and_NNW" departLane="free" departSpeed="max"/>  

Well it is a highway to hell but we yet need to make one more conversion, now to vehicle routes, see next chapter.

**Creating Routes**  
This step will convert each vehicle trip definition in a Shortest Path route for each vehicle. This step may take some time, but not too much. Create a configuration file and execute it.  
$ duarouter --trip-files snowdonia.trips.xml --net-file snowdonia.grid.net.xml --output-file snowdonia.rou.xml --taz-files snowdonia.taz.xml,snowdonia.vehicles.add.xml --with-taz --save-configuration snowdonia.duarouter.config.xml  
$ duarouter -c snowdonia.duarouter.config.xml  

There you can see an example of a vehicle route, the route edges list define each edge that the vehicle need to pass to accomplish its trip:  
> <vehicle id="771" type="taxi" depart="505.14" departLane="free" departSpeed="max" fromTaz="taxi_NW" toTaz="taxi_SW"><route edges="0/19to1/19 1/19to1/18 1/18to1/17 1/17to1/16 1/16to1/15 1/15to1/14 1/14to1/13 1/13to1/12 1/12to1/11 1/11to1/10 1/10to1/9 1/9to1/8 1/8to1/7 1/7to1/6 1/6to1/5 1/5to1/4 1/4to1/3 1/3to1/2 1/2to1/1 1/1to0/1"/></vehicle>  

Marvelous right!?! Now we can finally execute a simulation at SUMO. See below how or take a break and drink some coffee.

**Creating Simulation configuration file**  
This step create the configuration file that will be used when running the sumo simulation, it uses the grid network of Snowdonia and the routing file, I also added a connection port that will be used to connect with the emitter code.  
$ sumo --save-configuration snowdonia.sumo.cfg -n snowdonia.grid.net.xml -r snowdonia.rou.xml --remote-port 8813  

HaHa I got you, we only run the simulation in the next step.

### Run SUMO <a id="run-sumo"></a> [^](#toc "To top")  
Now you can run the simulation in two way, first in the console, the simulation run in a few seconds. Another way is running the sumo-gui interface, there you can view the vehicle trips inside the network and also can change some behavior of this view, like delay of step simulation and color of occupancy edges.  

Run on console:  
$ sumo -c snowdonia.sumo.cfg  

Run on GUI interface:  
$ sumo-gui -c snowdonia.sumo.cfg  

### Runnig experiment <a id="running-experiment"></a> [^](#toc "To top")  
To accomplish the task and make the vehicle GPS emission in the Snowdonia city I need to use [Traci Interface](http://www.sumo.dlr.de/wiki/TraCI/Interfacing_TraCI_from_Python). The developed script will first connect to sumo and them will analyze each vehicle that is running, keep its information (for example it type) and running time, and them emit a signal of GPS. After, each emission is send to API to validate and capture if the vehicle is at Snowdonia area. The script output some time information, the number of vehicles running and success and fail emissions.  

The default behavior is to run the emitter with the local server and without user interface. If you want to execute using the heroku API and with graphical interface use the second command line.

Run the below command at console (root/sumo folder)  
$ python run.py

Run the below command at console (root/sumo folder) to use heroku and sumo gui.  
$ python run.py --remote --sumo-gui