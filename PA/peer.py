import asyncio
import json
import hashlib
from datetime import datetime

NODES = ["000", "001", "010", "011", "100", "101", "110", "111"]
PORT_BASE = 5000

class PeerNode:
    def __init__(self, node_id):
        self.node_id = node_id
        self.port = PORT_BASE + int(node_id, 2)
        self.topics = {}  # Dictionary to store topics
        self.neighbors = self.get_neighbors(node_id)
        self.log_file = f"peer_{node_id}.log"

    async def start(self):
        """Start the node to listen for incoming connections asynchronously."""
        server = await asyncio.start_server(self.handle_client, 'localhost', self.port)
        async with server:
            print(f"Peer {self.node_id} listening on port {self.port}")
            await server.serve_forever()

    async def handle_client(self, reader, writer):
        """Asynchronously handle incoming requests."""
        data = await reader.read(1024)
        request = json.loads(data.decode())
        action = request['action']
        topic = request.get('topic')
        message = request.get('message')
        target_id = self.hash_topic(topic) if topic else None

        response = await self.process_request(action, topic, message, target_id)
        writer.write(response.encode())
        await writer.drain()
        writer.close()
        await writer.wait_closed()

    async def process_request(self, action, topic, message, target_id):
        """Process or forward requests based on action."""
        if target_id and target_id != self.node_id:
            response = await self.forward_request(target_id, action, topic, message)
        else:
            response = await self.handle_local_request(action, topic, message)
        return response

    async def handle_local_request(self, action, topic, message):
        """Handle actions locally."""
        if action == 'create_topic':
            topics = topic.split(',')  # Allow multiple topics to be created
            created_topics = []
            for t in topics:
                t = t.strip()  # Remove leading/trailing whitespace
                if t not in self.topics:
                    self.topics[t] = []
                    created_topics.append(t)
                    await self.notify_neighbors("create_topic", t)
                else:
                    return json.dumps({"error": "Topic already exists"})  # Return error immediately if any topic exists
            response = {"status": "Topics created", "topics": created_topics} if created_topics else {"error": "No new topics to create"}
        elif action == 'delete_topic':
            if topic in self.topics:
                del self.topics[topic]
                response = {"status": "Topic deleted"}
                await self.notify_neighbors("delete_topic", topic)
            else:
                response = {"error": "Topic not found"}
        elif action == 'publish':
            if topic in self.topics:
                self.topics[topic].append(message)
                response = {"status": "Message published"}
            else:
                response = {"error": "Topic not found"}
        elif action == 'subscribe':
            if topic in self.topics:
                response = {"status": "Subscribed to topic"}
            else:
                response = {"error": "Topic not found"}
        elif action == 'list_topics':
            response = {'topics': list(self.topics.keys())}
        else:
            response = {"error": "Action not supported"}
        self.log_event(action, topic, response)
        return json.dumps(response)

    async def notify_neighbors(self, action, topic):
        """Notify neighboring peers about the creation/deletion of a topic."""
        for neighbor in self.neighbors:
            try:
                port = PORT_BASE + int(neighbor, 2)
                reader, writer = await asyncio.open_connection('localhost', port)
                notification = json.dumps({"action": action, "topic": topic})
                writer.write(notification.encode())
                await writer.drain()
                writer.close()
                await writer.wait_closed()
            except ConnectionRefusedError:
                print(f"Could not notify neighbor {neighbor}: not reachable")

    async def forward_request(self, target_id, action, topic, message):
        """Forward requests to the target node."""
        try:
            port = PORT_BASE + int(target_id, 2)
            reader, writer = await asyncio.open_connection('localhost', port)
            request = json.dumps({"action": action, "topic": topic, "message": message})
            writer.write(request.encode())
            await writer.drain()
            response = await reader.read(1024)
            writer.close()
            await writer.wait_closed()
            return response.decode()
        except ConnectionRefusedError:
            return json.dumps({"error": f"Peer {target_id} is not reachable"})

    def hash_topic(self, topic):
        """Determine which peer should store the topic."""
        hash_val = int(hashlib.sha1(topic.encode()).hexdigest(), 16) % len(NODES)
        return NODES[hash_val]

    def get_neighbors(self, node_id):
        """Get a list of binary IDs that differ by one bit."""
        neighbors = []
        for i in range(len(node_id)):
            flipped_id = list(node_id)
            flipped_id[i] = '1' if node_id[i] == '0' else '0'
            neighbors.append(''.join(flipped_id))
        return neighbors

    def log_event(self, event_type, topic, response):
        """Log events to a file."""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"{timestamp} - {event_type} - Topic: {topic} - Response: {response}\n"
        with open(self.log_file, 'a') as log:
            log.write(log_entry)
        print(log_entry)  # Print to console for immediate feedback during testing

async def main():
    """Initialize peer nodes."""
    nodes = [PeerNode(node_id) for node_id in NODES]
    tasks = [node.start() for node in nodes]
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main())
