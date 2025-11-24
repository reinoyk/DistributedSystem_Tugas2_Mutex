<div id="top">

<div align="center">

# DISTRIBUTED-MUTEX-KV-STORE

*Robust Key-Value Store with Mutual Exclusion and Gossip Protocol*

<p align="center">
<img src="https://img.shields.io/github/last-commit/reinoyk/distributedsystem_tugas2_mutex?style=flat&logo=git&logoColor=white&color=0080ff" alt="last-commit">
<img src="https://img.shields.io/badge/Language-Python-3776AB?style=flat&logo=python&logoColor=white" alt="python">
<img src="https://img.shields.io/badge/Architecture-Distributed-orange" alt="architecture">
</p>

<em>Built with Python, Socket Programming, and Logical Clocks</em>

</div>
---

## Table of Contents

* [Overview](#overview)
* [Features](#features)
* [System Architecture](#system-architecture)
* [Project Structure](#project-structure)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
  * [Configuration](#configuration)
* [Usage](#usage)
  * [Running the Logger](#running-the-logger)
  * [Running Nodes](#running-nodes)
  * [Using the Client](#using-the-client)
* [Testing Scenarios](#testing-scenarios)
* [How to Contribute](#how-to-contribute)
* [License](#license)

---

## Overview

**Distributed-Mutex-KV-Store** is a distributed Key-Value storage system designed to demonstrate advanced concepts in distributed computing. It implements a **Gossip Protocol** for membership and failure detection, **Vector Clocks** for causal ordering, and a **Mutual Exclusion (Mutex)** mechanism to ensure data consistency during concurrent write operations.


This project allows multiple nodes to communicate over TCP/UDP, replicate data using lazy propagation, and resolve conflicts using a leader-based locking mechanism. It includes a centralized Logger to visualize the ordering of events (Physical vs. Lamport vs. Vector).

---

## Features

* 🔄 **Gossip Protocol:** Uses UDP heartbeats to maintain a membership list and detect node failures (`ALIVE`, `SUSPECT`, `DEAD`).
* 🔒 **Distributed Mutual Exclusion:** Implements a leader-based coordinator to handle `LOCK_REQ` and `LOCK_REL`, preventing race conditions during critical `PUT` operations.
* 🕰️ **Logical Clocks:**
  * **Lamport Timestamps:** For total ordering of events.
  * **Vector Clocks:** For capturing causal relationships and detecting concurrency.
* 💾 **Key-Value Store:** Supports `PUT` and `GET` operations with replication across nodes.
* 📊 **Event Logger:** A dedicated server that collects traces from all nodes to visualize the partial ordering of distributed events.
* ⚡ **Interactive Client:** A Python-based CLI tool to send commands, race concurrent requests, and benchmark latency.

---

## System Architecture

The system consists of three main components:

1.  **KV Nodes:** The core servers. They handle client requests (TCP), gossip with peers (UDP), and coordinate mutex locks.
2.  **Logger:** A standalone service that listens for event logs from nodes and prints them sorted by time and logical clocks.
3.  **KV Client:** An external script to interact with the cluster.

**Technologies Used:**
* **Python 3:** Core programming language.
* **Sockets:** `socket.SOCK_STREAM` (TCP) for RPCs and `socket.SOCK_DGRAM` (UDP) for Gossip.
* **Threading:** To handle concurrent listeners (UDP listener, TCP server, Interactive input).
* **JSON:** For message serialization.

---

## Project Structure

```text
├── logger/
│   ├── kv.py         # Logger implementation
│   └── run.sh        # Script to start the logger
├── node1/
│   ├── kv.py         # Node 1 source code
│   └── run.sh        # Script to run Node 1
├── node2/
│   ├── kv.py         # Node 2 source code
│   └── run.sh        # Script to run Node 2
├── node3/
│   ├── kv.py         # Node 3 source code
│   └── run.sh        # Script to run Node 3
├── program/
│   ├── kv.py         # Base KV Node implementation
│   └── kvclient.py   # Client CLI tool
└── testing/
    ├── kvclient.py   # Client for testing
    ├── test1.sh      # Basic PUT/GET test
    ├── test2.sh      # Consistency test
    └── test3.sh      # Race condition & Mutex test
```
# Getting Started

## Prerequisites

* Python 3.8+
* Network access between nodes (or localhost for testing)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/reinoyk/distributedsystem_tugas2_mutex.git
```

2. Navigate to the project directory:
```bash
cd distributedsystem_tugas2_mutex
```

## Configuration

The provided `run.sh` scripts use specific IP addresses (e.g., `192.168.122.x`). If running locally or on a different network, you must update the `--host`, `--peers`, and `--logger-addr` arguments in the `.sh` files.

## Usage

### Running the Logger

Start the logger first to capture all cluster events.
```bash
cd logger
./run.sh
# Or manually:
# python3 kv.py --logger --logger-tcp 5000 --numnodes 3
```

### Running Nodes

Open separate terminals for each node. Ensure parameters define a unique ID and ports.

**Node 1:**
```bash
cd node1
./run.sh
# Example args: python3 kv.py --id 1 --tcp 5001 --udp 6001 --host <IP> ...
```

**Node 2:**
```bash
cd node2
./run.sh
```

**Node 3:**
```bash
cd node3
./run.sh
```

### Using the Client

You can use the `kvclient.py` to interact with the cluster.

**Single Command:**
```bash
python3 program/kvclient.py --nodes <IP>:5001,<IP>:5002,<IP>:5003 cmd --node 0 "PUT color red"
```

**Interactive REPL:**
```bash
python3 program/kvclient.py --nodes <IP>:5001,<IP>:5002 repl
```

## Testing Scenarios

The `testing/` folder contains scripts to verify system behavior.

### 1. Basic Operations (`test1.sh`)

Verifies that a value written to Node 1 can be read from Node 2 (Replication).
```bash
cd testing
./test1.sh
```

### 2. Consistency Check (`test2.sh`)

Performs multiple writes and reads to ensure data consistency across the cluster.
```bash
./test2.sh
```

### 3. Race Conditions & Mutex (`test3.sh`)

This is the critical test for this project. It spawns concurrent threads attempting to write to the same key simultaneously.

* Without Mutex: The final value might be indeterminate or updates lost.
* With Mutex (Enabled): The system serializes the writes, ensuring the final state is consistent.
```bash
./test3.sh
```

**Note:** Ensure `--use-mutex 1` is set in your node configurations to pass `test3.sh` successfully.
