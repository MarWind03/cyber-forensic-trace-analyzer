class ProcessNode:
    def __init__(self, process_name, pid):
        self.process_name = process_name
        self.pid = pid
        self.children = []  # List untuk menampung Child Nodes (Multi-way Tree)

class ProcessTree:
    def __init__(self, root_process_name, root_pid):
        # Inisialisasi akar dari pohon proses (misal: "system" atau "init")
        self.root = ProcessNode(root_process_name, root_pid)

    # Fungsi Helper Rekursif untuk mencari Node tertentu berdasarkan PID
    def _find_node_recursive(self, current_node, pid):
        if current_node.pid == pid:
            return current_node
        
        for child in current_node.children:
            found = self._find_node_recursive(child, pid)
            if found:
                return found
        return None

    # Menambahkan proses anak (child) ke proses induk (parent) tertentu
    def insert_process(self, parent_pid, child_name, child_pid):
        parent_node = self._find_node_recursive(self.root, parent_pid)
        if parent_node:
            new_child = ProcessNode(child_name, child_pid)
            parent_node.children.append(new_child)
            return True
        return False

    # REKURSIF: Menampilkan seluruh struktur pohon proses (Pretty Print)
    def display_tree_recursive(self, current_node, level=0):
        indent = "    " * level
        print(f"{indent}└── [PID: {current_node.pid}] {current_node.process_name}")
        for child in current_node.children:
            self.display_tree_recursive(child, level + 1)

    # REKURSIF: Melacak ke atas dari mana virus berasal (Root Cause Analysis)
    # Mencari jalur dari root menuju ke proses berbahaya (malware_pid)
    def trace_root_cause_recursive(self, current_node, target_pid, path=None):
        if path is None:
            path = []
        
        # Tambahkan proses sekarang ke dalam jalur penelusuran
        new_path = path + [f"{current_node.process_name} (PID: {current_node.pid})"]
        
        if current_node.pid == target_pid:
            return new_path
        
        for child in current_node.children:
            result_path = self.trace_root_cause_recursive(child, target_pid, new_path)
            if result_path:
                return result_path
        return None


# =====================================================================
# 2. GRAPH STRUCTURE (Network Graph untuk Memetakan Aliran Serangan)
# =====================================================================
class NetworkGraph:
    def __init__(self):
        # Menggunakan Adjacency List (Dictionary berisikan Set)
        # Key: IP Address asal, Value: Set of IP Address tujuan
        self.adjacency_list = {}

    def add_device(self, ip_address):
        if ip_address not in self.adjacency_list:
            self.adjacency_list[ip_address] = set()

    def add_traffic_edge(self, source_ip, destination_ip):
        # Pastikan kedua node perangkat terdaftar di Graph
        self.add_device(source_ip)
        self.add_device(destination_ip)
        
        # Buat hubungan satu arah (Directed Graph) mencerminkan aliran data log
        self.adjacency_list[source_ip].add(destination_ip)

    def display_network_graph(self):
        print("\n--- PETA HUBUNGAN JARINGAN (Graph Adjacency List) ---")
        for device, connections in self.adjacency_list.items():
            if connections:
                print(f"Perangkat [{device}] mengirim data ke -> {list(connections)}")
            else:
                print(f"Perangkat [{device}] -> Tidak mengirim data ke mana pun")

    # REKURSIF: Melacak rute penyebaran infeksi terjauh (Depth-First Search / DFS)
    def trace_infection_path_recursive(self, current_ip, visited=None, path=None):
        if visited is None:
            visited = set()
        if path is None:
            path = []

        visited.add(current_ip)
        path.append(current_ip)

        longest_path = list(path)

        # Telusuri semua perangkat yang pernah dikirimi data oleh IP ini
        for neighbor in self.adjacency_list.get(current_ip, set()):
            if neighbor not in visited:
                # Rekursi untuk masuk lebih dalam ke cabang jaringan berikutnya
                new_path = self.trace_infection_path_recursive(neighbor, visited, path)
                if len(new_path) > len(longest_path):
                    longest_path = new_path

        # Backtrack (hapus dari path saat kembali dari rekursi)
        path.pop()
        return longest_path