#!/bin/bash
#

# Single PUT to node 1
python3 ./kvclient.py --nodes 127.0.0.1:8001,127.0.0.1:8002,127.0.0.1:8003 cmd --node 1  "PUT color black"
python3 ./kvclient.py --nodes 127.0.0.1:8001,127.0.0.1:8002,127.0.0.1:8003 cmd --node 2  "PUT color magenta"
python3 ./kvclient.py --nodes 127.0.0.1:8001,127.0.0.1:8002,127.0.0.1:8003 cmd --node 2  "PUT warna kuning"
python3 ./kvclient.py --nodes 127.0.0.1:8001,127.0.0.1:8002,127.0.0.1:8003 cmd --node 2  "PUT warna kuning"
python3 ./kvclient.py --nodes 127.0.0.1:8001,127.0.0.1:8002,127.0.0.1:8003 race "PUT color blue" "PUT color green" 
python3 ./kvclient.py --nodes 127.0.0.1:8001,127.0.0.1:8002,127.0.0.1:8003 race "PUT warna oranye" "PUT warna hijau" 


echo "-------HASIL----"
python3 ./kvclient.py --nodes 127.0.0.1:8001,127.0.0.1:8002,127.0.0.1:8003  getall color
echo "-------HASIL----"
python3 ./kvclient.py --nodes 127.0.0.1:8001,127.0.0.1:8002,127.0.0.1:8003  getall warna




