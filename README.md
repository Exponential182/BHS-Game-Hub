# BHS Game Hub

An alternative tool to itch.io for hosting games developed with the posibility of being used by Burnisde High School.

### Setup and Deployment
#### Normal Setup
 - Clone the repository
 - Create a virtual environment (optional)
 - Install the packages in __requirements.txt__
 - Run __app.py__ from this directory

#### Server Deployment (WIP)

First, REPLACE the secret key in app.py with a new random 256 bit hex string UNLESS you install the docker image directly.

Then either:
 - Download the repo and deploy it to any server as per the normal setup.

__OR__  
 - Compile the docker image using docker compose and the contained files.
 - Deploy this to your server

This is the preffered method for deployment if applicable because it allows Gunicorn and Nginx to be used for improved server perfomance and thread handling.
