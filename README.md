# Snowdonia challenge
For information about the challenge, see [CHALLENGE](https://github.com/advecchia/backend-code-challenge/blob/master/CHALLENGE.md) documentation.  
Below you can see information about how to setup your development environment and also how to deploy this code to [Heroku](https://www.heroku.com/). For traffic simulation I used [SUMO](http://sumo.dlr.de/userdoc/index.html) and [JOSM](https://josm.openstreetmap.de/), there is also a how to make your own simulation. For performance I chose [LOCUST](http://locust.io/).  

See below an architecture overview of the solution.  
![Snowdonia Architecture](https://raw.githubusercontent.com/advecchia/backend-code-challenge/master/docs/api/snowdonia_architecture.png "Snowdonia Architecture")  

### <a id="toc"></a>Table of Contents 
 * [Environment and Deploy](#environment-and-deploy)  
 * [Other documentations](#other-documentations)  

## Environment and Deploy <a id="environment-and-deploy"></a> [^](#toc "To top")  
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

## Other documentations <a id="other-documentations"></a> [^](#toc "To top")  
[API Description](https://github.com/advecchia/backend-code-challenge/blob/master/docs/api/README.md)  
[Performance Tests](https://github.com/advecchia/backend-code-challenge/blob/master/docs/performance/README.md)  
[SUMO Simulation Description](https://github.com/advecchia/backend-code-challenge/blob/master/docs/sumo/README.md)  