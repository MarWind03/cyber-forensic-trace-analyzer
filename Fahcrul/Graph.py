#Peta penyebaran serangan malware
class NetworkGraph:
    def __init__(self):
        self.connections = {}

    def add_device(self, ip):
        if ip not in self.connections:
            self.connections[ip] = []

    def add_connection(self, source_ip, destination_ip):
        self.add_device(source_ip)
        self.add_device(destination_ip)

        self.connections[source_ip].append(destination_ip)

    def display_graph(self):
        print("\n=== PETA KOMUNIKASI JARINGAN ===")

        for source, destinations in self.connections.items():
            print(f"{source} -> {destinations}")

#Contoh penggunaan
network_graph = NetworkGraph()

network_graph.add_connection(
    "185.220.101.5",
    "192.168.10.1"
)

network_graph.add_connection(
    "192.168.10.1",
    "192.168.10.50"
)

network_graph.display_graph()




#Rekursif pada graph
def trace_infection(graph, current_ip, visited=None):
    if visited is None:
        visited = set()

    visited.add(current_ip)

    print(current_ip)

    for neighbor in graph.connections.get(current_ip, []):

        if neighbor not in visited:
            trace_infection(
                graph,
                neighbor,
                visited
            )

#contoh
trace_infection(
    network_graph,
    "185.220.101.5"
)