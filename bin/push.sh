#!/usr/bin/env bash
# How to upload
./build.sh
docker push pyengine/google-cloud-stackdriver:1.0
docker push spaceone/google-cloud-stackdriver:1.0
