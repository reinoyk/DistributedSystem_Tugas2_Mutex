#!/bin/bash
#

# Single PUT to node 1 (Note: node 1 is index 0, node 2 is index 1, etc if using 0-based index in kvclient)
# But based on your previous mapping in kvclient, index 0=160 (node1), 1=188 (node2), 2=161 (node3)

python3 ./kvclient.py --nodes 192.168.122.160:5001,192.168.122.188:5002,192.168.122.161:5003 cmd --node 1  "PUT color red"
python3 ./kvclient.py --nodes 192.168.122.160:5001,192.168.122.188:5002,192.168.122.161:5003 cmd --node 2  "PUT color blue"


# GET from node 2
python3 ./kvclient.py  --nodes 192.168.122.160:5001,192.168.122.188:5002,192.168.122.161:5003 cmd --node 2   "GET color"
python3 ./kvclient.py  --nodes 192.168.122.160:5001,192.168.122.188:5002,192.168.122.161:5003 cmd --node 0   "GET color"