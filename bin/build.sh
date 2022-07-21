#! /bin/bash
# Build a docker image
cd ..
docker build -t pyengine/google-cloud-stackdriver . --no-cache
docker tag pyengine/google-cloud-stackdriver pyengine/google-cloud-stackdriver:1.0
docker tag pyengine/google-cloud-stackdriver spaceone/google-cloud-stackdriver:1.0
