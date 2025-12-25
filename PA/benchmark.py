import asyncio
import json
import random
import time
import sys
import matplotlib.pyplot as plt

# Constants
NODES = ["000", "001", "010", "011", "100", "101", "110", "111"]
PORT_BASE = 5000
TOPICS = [f"Topic{i}" for i in range(1, 21)]  # Sample topics for testing
ACTIONS = ["create_topic", "publish", "subscribe", "delete_topic"]
NUM_REQUESTS = 100  # Total requests for the benchmark
MEASUREMENTS = {"latencies": [], "throughputs": []}

async def send_request(action, node_id, topic=None, message=None):
    """Send a request to a specific node."""
    port = PORT_BASE + int(node_id, 2)  # Calculate the port based on node ID
    reader, writer = await asyncio.open_connection('localhost', port)

    request = {"action": action, "topic": topic, "message": message}
    writer.write(json.dumps(request).encode())
    await writer.drain()

    response = await reader.read(1024)
    writer.close()
    await writer.wait_closed()
    return response.decode()

async def benchmark():
    """Conduct the benchmarking tests."""
    for _ in range(NUM_REQUESTS):
        action = random.choice(ACTIONS)
        node_id = random.choice(NODES)
        topic = random.choice(TOPICS)
        message = f"Message for {topic}"

        start_time = time.time()
        response = await send_request(action, node_id, topic, message)
        end_time = time.time()

        latency = end_time - start_time
        MEASUREMENTS["latencies"].append(latency)

        # Check for successful actions
        result = json.loads(response)
        if "status" in result:
            MEASUREMENTS["throughputs"].append(1 / latency)  # Throughput = 1/latency

async def main():
    await benchmark()
    avg_latency = sum(MEASUREMENTS["latencies"]) / len(MEASUREMENTS["latencies"])
    avg_throughput = sum(MEASUREMENTS["throughputs"]) / len(MEASUREMENTS["throughputs"])
    
    print(f"Average Latency: {avg_latency:.4f} seconds")
    print(f"Average Throughput: {avg_throughput:.4f} requests/second")

    # Graphing the results
    plt.figure(figsize=(12, 6))
    
    # Latency plot
    plt.subplot(1, 2, 1)
    plt.plot(MEASUREMENTS["latencies"], label='Latency', color='blue')
    plt.title('Latency over Requests')
    plt.xlabel('Request Number')
    plt.ylabel('Latency (seconds)')
    plt.grid(True)
    plt.legend()

    # Throughput plot
    plt.subplot(1, 2, 2)
    plt.plot(MEASUREMENTS["throughputs"], label='Throughput', color='green')
    plt.title('Throughput over Requests')
    plt.xlabel('Request Number')
    plt.ylabel('Throughput (requests/second)')
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.savefig("benchmark_results.png")
    plt.show()

if __name__ == '__main__':
    asyncio.run(main())
