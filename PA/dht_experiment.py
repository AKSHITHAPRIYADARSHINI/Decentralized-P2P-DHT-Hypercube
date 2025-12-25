import random
import matplotlib.pyplot as plt

class Node:
    def __init__(self, node_id):
        self.node_id = node_id
        self.routing_table = {}
        self.data_store = {}
        self.reputation_score = 100  # Start with a perfect score

    def store_data(self, key, value):
        self.data_store[key] = value

    def lookup_data(self, key):
        return self.data_store.get(key, None)

class DHT:
    def __init__(self):
        self.nodes = {}
        self.attack_metrics = {
            "sybil": [],
            "eclipse": [],
            "reputation": [],
            "integrity": [],
        }

    def add_node(self, node):
        self.nodes[node.node_id] = node

    def perform_lookup(self, key):
        # Simulate a lookup, returning None if not found
        for node in self.nodes.values():
            value = node.lookup_data(key)
            if value is not None:
                return value
        return None

    def run_sybil_attack(self, number_of_fake_nodes):
        for i in range(number_of_fake_nodes):
            fake_node = Node(node_id=f"fake_{i}")
            self.add_node(fake_node)

    def run_eclipse_attack(self, target_node_id):
        if target_node_id in self.nodes:
            target_node = self.nodes[target_node_id]
            # Simulate an eclipse by surrounding it with malicious nodes
            for i in range(5):  # Add 5 malicious nodes
                malicious_node = Node(node_id=f"malicious_{i}")
                self.add_node(malicious_node)
                # Connect malicious nodes to the target node's routing table
                target_node.routing_table[malicious_node.node_id] = malicious_node

    def evaluate_reputation(self):
        # Example logic to evaluate and decrease reputation scores
        for node in self.nodes.values():
            if random.random() < 0.2:  # 20% chance to lose reputation
                node.reputation_score -= random.randint(1, 50)

    def check_data_integrity(self, key):
        # Simulate a data integrity check
        return random.choice([True, False])  # Randomly return True or False

# Simulation Setup
def simulate_dht_experiment():
    dht = DHT()
    # Create legitimate nodes
    for i in range(10):
        dht.add_node(Node(node_id=f"legit_{i}"))

    # Store some data
    for i in range(50):
        dht.nodes[f"legit_{random.randint(0, 9)}"].store_data(f"key_{i}", f"value_{i}")

    # Baseline performance
    baseline_lookups = []
    for i in range(20):
        key = f"key_{random.randint(0, 49)}"
        result = dht.perform_lookup(key)
        baseline_lookups.append(result)

    # Run Sybil attack
    dht.run_sybil_attack(10)
    sybil_lookups = []
    for i in range(20):
        key = f"key_{random.randint(0, 49)}"
        result = dht.perform_lookup(key)
        sybil_lookups.append(result)

    # Run Eclipse attack
    dht.run_eclipse_attack(target_node_id="legit_0")
    eclipse_lookups = []
    for i in range(20):
        key = f"key_{random.randint(0, 49)}"
        result = dht.perform_lookup(key)
        eclipse_lookups.append(result)

    # Evaluate reputation system
    dht.evaluate_reputation()
    reputation_scores = [node.reputation_score for node in dht.nodes.values()]
    dht.attack_metrics["reputation"].append(reputation_scores)

    # Check data integrity
    integrity_checks = [dht.check_data_integrity(f"key_{i}") for i in range(50)]
    dht.attack_metrics["integrity"].append(sum(integrity_checks) / len(integrity_checks))

    return baseline_lookups, sybil_lookups, eclipse_lookups, dht.attack_metrics

# Running the experiment
baseline, sybil, eclipse, metrics = simulate_dht_experiment()

# Data Visualization
def plot_results(baseline, sybil, eclipse, metrics):
    plt.figure(figsize=(12, 6))

    # Lookup Results
    plt.subplot(1, 2, 1)
    plt.plot(baseline, label='Baseline Lookups', marker='o')
    plt.plot(sybil, label='Sybil Attack Lookups', marker='o')
    plt.plot(eclipse, label='Eclipse Attack Lookups', marker='o')
    plt.title('DHT Lookup Results')
    plt.xlabel('Lookup Attempts')
    plt.ylabel('Values Found')
    plt.legend()

    # Reputation and Integrity
    plt.subplot(1, 2, 2)
    plt.plot(metrics["reputation"][0], label='Reputation Scores', marker='o')
    plt.axhline(y=50, color='r', linestyle='--', label='Reputation Threshold')
    plt.title('Node Reputation Scores After Attacks')
    plt.xlabel('Node Index')
    plt.ylabel('Reputation Score')
    plt.legend()

    plt.tight_layout()
    plt.show()

# Call to plot the results
plot_results(baseline, sybil, eclipse, metrics)

