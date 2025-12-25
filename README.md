# Decentralised Peer-to-Peer System

## Introduction

This project implements a decentralized P2P system built upon a distributed hash table (DHT) with a hypercube topology. It provides an in-depth analysis of the peer node architecture, communication mechanisms, and request routing strategy. Additionally, the report evaluates the system’s performance through experiments assessing API functionality, latency, throughput, topic distribution, and request forwarding efficiency, supported by benchmark results and graphical analyses.

## Table of Contents
- [Features](#features)
- [Components](#files)
- [Technology & Libraries](#technologies&libraries)
- [Installation](#installation)
- [Project Structure](#order)
- [Usage](#running-the-application)

## Features
- **Decentralized Architecture**: The system uses a decentralized P2P architecture, allowing peer nodes to independently host and manage topics without relying on a central server.
- **Topic Management**: Peers can create, delete, and list topics, enabling dynamic topic management.
- **Message Publishing**: Peers can publish messages to specific topics, facilitating communication within the network.
- **Subscription Mechanism**: Peers can subscribe to topics to receive messages, allowing for real-time updates on relevant subjects.
- **Routing Mechanism**: Requests are routed to the appropriate peer nodes based on a distributed hash table (DHT), ensuring efficient message handling.
- **Neighbor Notification**: When topics are created or deleted, peers notify neighboring peers to maintain consistency in topic management.
- **Error Handling**: The system includes error handling for unreachable peers and invalid actions, enhancing robustness.
- **Logging**: Events are logged to a file for auditing and debugging purposes, providing insight into system operations.
- **Benchmarking Capabilities**: The system includes a benchmarking script to measure API functionality, latency, and throughput, allowing for performance evaluation.
- **Graphical Analysis**: Visualization of benchmarking results using Matplotlib, aiding in the analysis of system performance metrics.

## Components
-**peer.py**: Implements a peer node in a decentralized P2P system using a distributed hash table and hypercube topology. Each peer can create, delete, publish, and subscribe to topics, communicate with neighboring peers, and handle incoming requests asynchronously.

-**client.py**: Provides a command-line interface for users to interact with peer nodes. It supports topic creation, deletion, message publishing, subscription to topics, and listing all available topics on a peer.

-**benchmark.py**: Benchmarks the system's performance by simulating multiple requests (e.g., topic creation, publishing, subscription) to evaluate latency and throughput. It also generates graphical representations of latency and throughput results using Matplotlib.

## Technologies & Libraries
- Python 3.x : The primary programming language used for the entire project.
- Visual Studio Code (VS Code) with Python extensions (for IDE-based development)
- Distributed Hash Table (DHT): Used as the data structure for distributing and locating topics across nodes in a decentralized manner.
- Hypercube Topology: Implements peer-to-peer connections by linking nodes in a structure where each peer has neighbors differing by one binary digit, enabling efficient request routing.
- Asynchronous I/O: Provides non-blocking communication and processing, which allows the system to handle multiple simultaneous requests and maintain responsiveness.
- Command-Line Interface (CLI): Facilitates user interaction with the system through commands to create, delete, publish, and subscribe to topics.
- Asyncio: Enables asynchronous programming, allowing concurrent handling of multiple requests in the P2P system.
- Json: Handles JSON data for communication between peer nodes and clients, encoding requests and decoding responses.
- Hashlib: Generates SHA-1 hash values for topic names, which determine topic storage locations in the DHT.
- Datetime: Provides timestamps for logging events in each peer node.
- Random: Generates random selections for topics, actions, and nodes in the benchmark testing.
- Time: Measures latency by calculating the time taken to process requests in benchmarking.


## Installation
**Step 1: Install Python and Pip
Make sure you have Python 3.x and pip installed.

For Ubuntu/Debian:

bash
[Copy code]
sudo apt update
sudo apt install python3 python3-pip

For CentOS/Fedora:

bash
[Copy code]
sudo yum install python3 python3-pip

Verify installation:

bash
[Copy code]
python3 --version
pip3 --version

**Step 2: Install Required Libraries

Use pip to install Flask, AIOHTTP, and Matplotlib:

bash
[Copy code]
pip3 install flask aiohttp matplotlib

(or)

pip3 install -r requirements.txt
from the document made in the PA2 zip file.

## Project Structure 
- `peer.py`: Defines peer nodes with topic hosting, publishing, and forwarding capabilities.
- `client.py`: Allows users to interact with the P2P network by sending various requests to peer nodes.
- `benchmark.py`: Conducts performance tests on the network, measuring latency and throughput with graphical analysis.


## Usage
--**Step 1**: Starting the Peer Network

1. Open a terminal window.
2. Run peer.py to initialize all peer nodes:
bash
[Copy code]
python peer.py
Each node will begin listening on its unique port for incoming connections.

--**Step 2**: Using the Client

To run client.py, use the following format:
bash
[Copy code]
python client.py <action> <node_id(s)> [<topic>] [<message>]

**Available Actions**
1. `Create Topic`
Description: Creates a new topic on specified peer nodes.
Format: create_topic <node_id(s)> <topic>
Example:
bash
[Copy code]
python client.py create_topic 000 Topic1
Explanation: This command creates Topic1 on peer nodes 000 and 001.

2. `Delete Topic`
Description: Deletes an existing topic from a specific peer node.
Format: delete_topic <node_id> <topic>
Example:
bash
[Copy code]
python client.py delete_topic 000 Topic1
Explanation: This command deletes Topic1 from peer node 000.

3. `Publish Message`
Description: Publishes a message to a specific topic on a peer node.
Format: publish <node_id> <topic> <message>
Example:
bash
[Copy code]
python client.py publish 000 Topic1 "Hello, this is a message"
Explanation: This command publishes "Hello, this is a message" to Topic1 on peer node 000.

4. 'Subscribe to Topic'
Description: Subscribes to a topic on a specific peer node.
Format: subscribe <node_id> <topic>
Example:
bash
[Copy code]
python client.py subscribe 000 Topic1
Explanation: This command subscribes to Topic1 on peer node 000.

5. 'List Topics'
Description: Lists all topics available on a specified peer node.
Format: list_topics <node_id>
Example:
bash
[Copy code]
python client.py list_topics 000
Explanation: This command retrieves a list of all topics hosted on peer node 000


--**Step 3**: Benchmark the System

Open a separate terminal and execute benchmark.py to assess latency and throughput:
bash
[Copy code]
python benchmark.py
------------------------------------------------------------------------------------------------------------------------------------------

-------------------------------------------------- DHT Experiment -----------------------------------------------------
Report on Security Vulnerabilities in Distributed Hash Tables (DHTs):

-**Introduction**
Distributed Hash Tables (DHTs) are crucial components of many decentralized systems, particularly in peer-to-peer networks. While they provide efficient storage and retrieval of data, DHTs are susceptible to various security vulnerabilities. This report investigates the most prevalent security threats to DHTs, specifically focusing on Sybil and eclipse attacks. Additionally, it examines the effectiveness of existing mitigation strategies, including peer reputation systems and data integrity checks.

-**Experimental Setup**
- 'DHT Implementation' : A basic DHT structure was implemented using Python, allowing nodes to join, leave, store key-value pairs, and perform lookups.
- 'Attack Simulations' : The following attacks were simulated:
- 'Sybil Attack' : Multiple fake nodes were generated to infiltrate the network.
- 'Eclipse Attack' : A legitimate node was surrounded by malicious nodes to isolate it from the network.
- 'Countermeasures' : The following countermeasures were implemented:
- 'Peer Reputation System' : Nodes maintained reputation scores based on successful interactions.
- 'Data Integrity Checks' : Cryptographic hashes were used to verify data integrity during lookups.

**Tools and Environment**
- 'Programming Language': Python
- 'Development Environment': Visual Studio Code
- 'Libraries Used': Twisted for networking (optional), matplotlib for data visualization.

**Setup Instructions**

1. Install Python: Ensure Python is installed on your system. You can download it from python.org.

2. Install Required Libraries: Open your terminal or command prompt and execute the following command:
bash
[Copy code]
pip install matplotlib
Create a New Python File: Open your preferred text editor or Integrated Development Environment (IDE), such as Visual Studio Code, and create a new file named dht_experiment.py

**Running the Code**
1. Open Terminal or Command Prompt: Navigate to the directory where dht_experiment.py is located.

2. Execute the Script: Run the following command in your terminal:
bash
[Copy code]
python dht_experiment.py

View Results: Upon running the script, two plots will be displayed:

The left plot shows the results of lookups during baseline, Sybil, and eclipse attack conditions.
The right plot illustrates the reputation scores of nodes after the attacks, along with a threshold line for reference.
------------------------------------------------------------------------------------------------------------------------------------------
