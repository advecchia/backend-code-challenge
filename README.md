# Snowdonia challenge
For information about the challenge, see [CHALLENGE](https://github.com/advecchia/backend-code-challenge/blob/master/CHALLENGE.md) documentation.

See below the instructions for setup a experiment, run and visualize the simulation results.
TBD.

## Development environment
Assuming a Ubuntu OS.
Install Python, Gunicorn, Locust, Sumo, JOSM, ~~Sqlite3~~, PostgreSQL

sudo apt-get update
sudo apt-get install postgresql

## SUMO - Simulation For Urban Mobility
netconvert --type-files osmNetconvert.typ.xml --osm-files snowdonia.osm.xml --output-file snowdonia.net.xml --remove-edges.isolated --roundabouts.guess --ramps.guess

### Environment configuration
 
### Generating Network

### Generating Traffic and trips

### Run simulation

## Deploy on Heroku

Test locally
heroku local

Adding PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev
heroku config:set WEB_CONCURRENCY=3

## Performance Tests
locust -f performance.py --host=http://0.0.0.0:5000

## Challenges
After up and running local application and Heroku deploy crashing every time because of a port problem I learn that it can not deal with Sqlite database, so I need to change database to PostgreSQL. 