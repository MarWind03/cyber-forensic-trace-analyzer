#Rekursif melacak asal penyebaran pada graph
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
"""trace_infection(
    network_graph,
    "185.220.101.5"
)"""


#Rekrusif menampilkan tree
def display_process_tree(node, level=0):
    print("   " * level + node.process_name)

    for child in node.children:
        display_process_tree(child, level + 1)




#Rekursif mencari root penyebab infeksi dalam tree
def find_root_process(node):
    if node is None:
        return None

    if not hasattr(node, "parent"):
        return node

    if node.parent is None:
        return node

    return find_root_process(node.parent)


