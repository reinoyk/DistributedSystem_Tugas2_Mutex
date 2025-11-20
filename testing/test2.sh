#!/bin/bash
#

# Single PUT to node 1
python3 ./kvclient.py --nodes 127.0.0.1:8001,127.0.0.1:8002,127.0.0.1:8003 cmd --node 1  "PUT color red"
python3 ./kvclient.py --nodes 127.0.0.1:8001,127.0.0.1:8002,127.0.0.1:8003 cmd --node 2  "PUT color blue"


# GET from node 2
python3 ./kvclient.py  --nodes 127.0.0.1:8001,127.0.0.1:8002,127.0.0.1:8003 cmd --node 2   "GET color"
python3 ./kvclient.py  --nodes 127.0.0.1:8001,127.0.0.1:8002,127.0.0.1:8003 cmd --node 0   "GET color"




