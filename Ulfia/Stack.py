class InvestigationStack:
    def __init__(self):
        self.top = None
        self.history_count = 0

    def push(self, ip_address):
        """Membuka detail IP (Push ke stack)"""
        new_node = Node(ip_address)
        new_node.next = self.top
        self.top = new_node
        self.history_count += 1

        print(f"[STACK] Membuka investigasi: {ip_address}")

def pop(self):
        """Tombol Back (Pop dari stack)"""
        if self.top is None:
            print("[STACK] Riwayat kosong, tidak bisa kembali.")
            return None
        
        popped_ip = self.top.data
        self.top = self.top.next
        self.history_count -= 1
        
        print(f"[STACK] < BACK ... Keluar dari investigasi: {popped_ip}")
        return popped_ip

def peek(self):
        """Lihat IP yang sedang diselidiki saat ini"""
        if self.top:
            return self.top.data
        return "Halaman Utama Dashboard"