import asyncio
import json
import sys

async def send_request(action, node_id, topic=None, message=None):
    port = 5000 + int(node_id, 2)  # Calculate the port based on node ID
    reader, writer = await asyncio.open_connection('localhost', port)

    request = {"action": action, "topic": topic, "message": message}
    writer.write(json.dumps(request).encode())
    await writer.drain()

    response = await reader.read(1024)
    writer.close()
    await writer.wait_closed()
    return response.decode()

async def main():
    if len(sys.argv) < 3:
        print("Usage: client.py <action> <node_ids> [<topic>] [<message>]")
        print("Actions:")
        print("  create_topic - Create a new topic on multiple nodes (comma-separated node IDs)")
        print("  delete_topic - Delete an existing topic on a specific node")
        print("  publish      - Publish a message to a topic on a specific node")
        print("  subscribe    - Subscribe to a topic on a specific node")
        print("  list_topics  - List all topics on a specific node")
        return

    action = sys.argv[1]

    if action == "list_topics":
        if len(sys.argv) != 3:
            print("Usage: client.py list_topics <node_id>")
            return

        node_id = sys.argv[2]
        response = await send_request(action, node_id)
        print(f"Response from Peer {node_id}: {response}")
        return

    node_ids = sys.argv[2].split(',')  # Get multiple node IDs
    topic = sys.argv[3] if len(sys.argv) > 3 else None
    message = sys.argv[4] if len(sys.argv) > 4 else None

    # Input validation for actions
    if action == "create_topic":
        # Create topic on multiple nodes
        for node_id in node_ids:
            response = await send_request(action, node_id, topic)
            print(f"Response from Peer {node_id}: {response}")
    else:
        # For other actions, assume they're to be sent to a single node
        if len(node_ids) > 1:
            print("For actions other than create_topic, please specify only one node ID.")
            return
        
        node_id = node_ids[0]
        if action in ["publish", "subscribe"] and not topic:
            print("Topic must be specified for publish and subscribe actions.")
            return

        if action == "publish" and not message:
            print("Message must be specified for publish action.")
            return

        response = await send_request(action, node_id, topic, message)
        print(f"Response from Peer {node_id}: {response}")

if __name__ == '__main__':
    asyncio.run(main())
