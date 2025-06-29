# Enum for server health status
from enum import Enum

class ServerStatus(Enum):
    HEALTHY = True
    UNHEALTHY = False

# ---------------------------------------------
# Server class
# ---------------------------------------------
class Server:
    def __init__(self, server_id):
        self.server_id = server_id
        self.status = ServerStatus.HEALTHY

    def is_healthy(self):
        return self.status == ServerStatus.HEALTHY

    def set_status(self, status):
        self.status = status

    def get_server_id(self):
        return self.server_id

# ---------------------------------------------
# Request class (can be expanded as needed)
# ---------------------------------------------
class Request:
    pass

# ---------------------------------------------
# Strategy Pattern Interface
# ---------------------------------------------
class LoadBalancingStrategy:
    def get_server(self, servers, request):
        raise NotImplementedError

# ---------------------------------------------
# Round Robin Strategy
# ---------------------------------------------
class RoundRobinStrategy(LoadBalancingStrategy):
    def __init__(self):
        self.index = 0

    def get_server(self, servers, request):
        healthy_servers = [s for s in servers if s.is_healthy()]
        if not healthy_servers:
            raise Exception("No healthy servers available")

        server = healthy_servers[self.index % len(healthy_servers)]
        self.index += 1
        return server

# ---------------------------------------------
# Least Connections Strategy
# ---------------------------------------------
class LeastConnectionsStrategy(LoadBalancingStrategy):
    def __init__(self):
        self.connections = {}

    def get_server(self, servers, request):
        healthy_servers = [s for s in servers if s.is_healthy()]
        if not healthy_servers:
            raise Exception("No healthy servers available")

        # Assign zero if not tracked
        for s in healthy_servers:
            self.connections.setdefault(s.get_server_id(), 0)

        selected_server = min(healthy_servers, key=lambda s: self.connections[s.get_server_id()])
        self.connections[selected_server.get_server_id()] += 1
        return selected_server

# ---------------------------------------------
# Singleton LoadBalancer
# ---------------------------------------------
class LoadBalancer:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LoadBalancer, cls).__new__(cls)
            cls._instance.servers = []
            cls._instance.strategy = None
        return cls._instance

    def add_server(self, server):
        self.servers.append(server)

    def remove_server(self, server):
        self.servers.remove(server)

    def set_strategy(self, strategy):
        self.strategy = strategy

    def get_server(self, request):
        if not self.strategy:
            raise Exception("No load balancing strategy set")
        return self.strategy.get_server(self.servers, request)

# ---------------------------------------------
# Driver code
# ---------------------------------------------
if __name__ == '__main__':
    # Create servers
    s1 = Server("Server1")
    s2 = Server("Server2")

    # Initialize load balancer (singleton)
    lb = LoadBalancer()
    lb.add_server(s1)
    lb.add_server(s2)

    # Set strategy (you can switch to LeastConnectionsStrategy())
    lb.set_strategy(RoundRobinStrategy())

    # Send some requests
    for i in range(5):
        req = Request()
        selected = lb.get_server(req)
        print(f"Request {i+1} routed to: {selected.get_server_id()}")
