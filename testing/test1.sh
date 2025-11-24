#!/bin/bash
#

# Single PUT to node 1
python3 ./kvclient.py --nodes 192.168.122.161:5001,192.168.122.188:5002,192.168.122.160:5003 cmd --node 1  "PUT color blue"


# GET from node 2
python3 ./kvclient.py  --nodes 192.168.122.161:5001,192.168.122.188:5002,192.168.122.160:5003 cmd --node 2   "GET color"


# Race two writers (great for no-mutex demo)
python3 ./kvclient.py --nodes 192.168.122.161:5001,192.168.122.188:5002,192.168.122.160:5003 race  "PUT color blue" "PUT color red"


# Read the key from ALL nodes after the race
python3 ./kvclient.py --nodes 192.168.122.161:5001,192.168.122.188:5002,192.168.122.160:5003  getall color