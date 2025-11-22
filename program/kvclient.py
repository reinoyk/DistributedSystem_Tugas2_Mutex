#!/usr/bin/env python3
"""
MODIFIED FOR SPECIFIC IPs:
Node 1: 192.168.122.160:5001
Node 2: 192.168.122.188:5002
Node 3: 192.168.122.161:5003
"""

import argparse, socket, time, threading, random, statistics, sys
from typing import List, Tuple

# --------------------- TCP helpers ---------------------

def send_cmd(host: str, port: int, cmd: str, timeout: float=2.0) -> str:
    t0 = time.perf_counter()
    with socket.create_connection((host, port), timeout=timeout) as s:
        s.sendall((cmd + "\n").encode())
        s.shutdown(socket.SHUT_WR)
        data = s.recv(65535)
    dt = (time.perf_counter() - t0) * 1000.0
    return data.decode().strip(), dt

# --------------------- Actions -------------------------

def action_cmd(nodes: List[Tuple[str,int]], node_idx: int, cmd: str):
    host, port = nodes[node_idx]
    out, dt = send_cmd(host, port, cmd)
    print(f"[{host}:{port}] {cmd} -> {out} ({dt:.2f} ms)")


def action_race(nodes: List[Tuple[str,int]], cmd1: str, cmd2: str):
    if len(nodes) < 2:
        print("Need at least 2 nodes for a race.")
        return
    # Use Node 2 and Node 3 for racing (as per common scenario) or just first two
    i1, i2 = 0, 1
    host1, port1 = nodes[i1]
    host2, port2 = nodes[i2]
    res = {}
    def tfunc(key, host, port, cmd):
        try:
            out, dt = send_cmd(host, port, cmd)
            res[key] = (out, dt)
        except Exception as e:
            res[key] = (f"ERR: {e}", 0)
    t1 = threading.Thread(target=tfunc, args=('A', host1, port1, cmd1))
    t2 = threading.Thread(target=tfunc, args=('B', host2, port2, cmd2))
    t1.start(); t2.start(); t1.join(); t2.join()
    print(f"[{host1}:{port1}] {cmd1} -> {res['A'][0]} ({res['A'][1]:.2f} ms)")
    print(f"[{host2}:{port2}] {cmd2} -> {res['B'][0]} ({res['B'][1]:.2f} ms)")


def action_getall(nodes: List[Tuple[str,int]], key: str):
    for (h,p) in nodes:
        try:
            out, dt = send_cmd(h, p, f"GET {key}")
            print(f"[{h}:{p}] GET {key} -> {out} ({dt:.2f} ms)")
        except Exception as e:
            print(f"[{h}:{p}] GET {key} -> ERROR {e}")


def action_bench(nodes: List[Tuple[str,int]], ops: int, key: str, put_ratio: float):
    lat = []
    puts = gets = 0
    for i in range(ops):
        h,p = random.choice(nodes)
        do_put = random.random() < put_ratio
        try:
            if do_put:
                val = f"v{i}"
                out, dt = send_cmd(h, p, f"PUT {key} {val}")
                puts += 1
            else:
                out, dt = send_cmd(h, p, f"GET {key}")
                gets += 1
            lat.append(dt)
        except:
            pass
    if lat:
        print(f"ops={ops} puts={puts} gets={gets} avg={statistics.mean(lat):.2f} ms p95={statistics.quantiles(lat, n=20)[18]:.2f} ms max={max(lat):.2f} ms")

# --------------------- REPL ----------------------------

def action_repl(nodes: List[Tuple[str,int]]):
    print("KV REPL. cmds: help | nodes | use <idx> | cmd <raw> | getall <key> | race <cmd1> | <cmd2> | quit")
    cur = 0
    while True:
        try:
            line = input(f"(node#{cur})> ").strip()
        except EOFError:
            break
        if not line:
            continue
        if line == 'quit':
            break
        if line == 'help':
            print("nodes -> list nodes; use <i> -> choose node; cmd <raw> -> send; getall <k>; race <cmd1> | <cmd2>")
            continue
        if line == 'nodes':
            for i,(h,p) in enumerate(nodes):
                print(f"  [{i}] {h}:{p}")
            continue
        if line.startswith('use '):
            try:
                cur = int(line.split()[1])
                if cur < 0 or cur >= len(nodes):
                    print("bad index")
                    cur = 0
            except Exception:
                print("usage: use <idx>")
            continue
        if line.startswith('cmd '):
            cmd = line[4:]
            h,p = nodes[cur]
            try:
                out, dt = send_cmd(h, p, cmd)
                print(f"[{h}:{p}] {cmd} -> {out} ({dt:.2f} ms)")
            except Exception as e:
                 print(f"Error: {e}")
            continue
        if line.startswith('getall '):
            key = line.split(' ',1)[1]
            action_getall(nodes, key)
            continue
        if line.startswith('race '):
            try:
                payload = line[5:]
                c1, c2 = [x.strip() for x in payload.split('|',1)]
                action_race(nodes, c1, c2)
            except Exception:
                print("usage: race <cmd1> | <cmd2>")
            continue
        print("unknown cmd; type 'help'")

# --------------------- Main ----------------------------

def parse_nodes(s: str) -> List[Tuple[str,int]]:
    out = []
    for tok in s.split(','):
        h,p = tok.split(':'); out.append((h, int(p)))
    return out

if __name__ == '__main__':
    # DEFAULT IPs Updated based on your request
    MY_NODES = "192.168.122.160:5001,192.168.122.188:5002,192.168.122.161:5003"

    ap = argparse.ArgumentParser(description='kv client')
    # Changed required=True to False, and added default
    ap.add_argument('--nodes', required=False, default=MY_NODES, help='comma list of host:port')

    sub = ap.add_subparsers(dest='mode', required=True)

    sp = sub.add_parser('cmd', help='send a single raw command to a chosen node')
    sp.add_argument('--node', type=int, default=0, help='node index (0-based)')
    sp.add_argument('raw', nargs=argparse.REMAINDER, help='raw command after --')

    sp = sub.add_parser('race', help='race two commands to first two nodes')
    sp.add_argument('cmd1')
    sp.add_argument('cmd2')

    sp = sub.add_parser('getall', help='GET a key from all nodes')
    sp.add_argument('key')

    sp = sub.add_parser('bench', help='simple latency benchmark')
    sp.add_argument('--ops', type=int, default=50)
    sp.add_argument('--key', default='color')
    sp.add_argument('--put-ratio', type=float, default=0.5)

    sp = sub.add_parser('repl', help='interactive shell')

    args = ap.parse_args()
    nodes = parse_nodes(args.nodes)

    if args.mode == 'cmd':
        raw = ' '.join(args.raw).strip()
        if not raw:
            print("provide a command after --, e.g., -- cmd \"PUT k v\"")
            sys.exit(2)
        action_cmd(nodes, args.node, raw)
    elif args.mode == 'race':
        action_race(nodes, args.cmd1, args.cmd2)
    elif args.mode == 'getall':
        action_getall(nodes, args.key)
    elif args.mode == 'bench':
        action_bench(nodes, args.ops, args.key, args.put_ratio)
    elif args.mode == 'repl':
        action_repl(nodes)