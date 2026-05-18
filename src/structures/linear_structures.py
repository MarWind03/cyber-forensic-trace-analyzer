class Node:
    def __init__(self, ip_address):
        self.ip_address = ip_address
        self.next = None

class InvestigationStack:
    def __init__(self):
        self.head = None  # Pointer ke node paling atas stack

    def push_history(self, ip_address):
        new_node = Node(ip_address)

        # Node baru menunjuk ke head lama
        new_node.next = self.head

        # Head berpindah ke node baru
        self.head = new_node

        print(f"Membuka investigasi untuk perangkat: {ip_address}")

    def pop_history(self):
        if self.head is None:
            print("Stack kosong.")
            return None

        # Jika hanya ada satu halaman
        if self.head.next is None:
            print("Anda berada di halaman utama investigasi. Tidak bisa kembali.")
            return None

        # Simpan halaman saat ini
        current_page = self.head.ip_address

        # Head mundur ke node berikutnya
        self.head = self.head.next

        previous_page = self.head.ip_address

        print(f"Kembali dari {current_page} ke perangkat: {previous_page}")

        return previous_page

    def is_empty(self):
        return self.head is None

    def show_stack(self):
        current = self.head

        if current is None:
            print("Stack kosong.")
            return

        print("Riwayat Investigasi:")
        while current:
            print(f"- {current.ip_address}")
            current = current.next



class Node:
    def __init__(self, server_ip):
        self.server_ip = server_ip
        self.next = None


class IncidentQueue:
    def __init__(self):
        self.front = None  # Pointer depan antrean
        self.rear = None   # Pointer belakang antrean
        self.size = 0

    # Masukkan server ke antrean (enqueue)
    def enqueue_incident(self, server_ip):
        new_node = Node(server_ip)

        # Jika antrean kosong
        if self.rear is None:
            self.front = self.rear = new_node
        else:
            # Sambungkan node baru ke belakang
            self.rear.next = new_node
            self.rear = new_node

        self.size += 1

        print(f"[ALERT] {server_ip} dimasukkan ke antrean penanganan bahaya!")

    # Keluarkan server dari antrean (dequeue)
    def dequeue_incident(self):
        if self.front is None:
            print("Aman! Tidak ada antrean insiden siber aktif.")
            return None

        handled_server = self.front.server_ip

        # Geser front ke node berikutnya
        self.front = self.front.next

        # Jika antrean menjadi kosong
        if self.front is None:
            self.rear = None

        self.size -= 1

        print(f"[REMEDIATION] Mulai membersihkan malware pada: {handled_server}")

        return handled_server

    # Tampilkan isi antrean
    def display_queue(self):
        if self.front is None:
            print("Antrean insiden kosong.")
            return

        print(f"\n--- ANTREAN RESPONS INSIDEN (Total: {self.size}) ---")

        current = self.front
        index = 1

        while current:
            print(f"{index}. Urutan Penanganan -> {current.server_ip}")
            current = current.next
            index += 1


# --- 2. Uji Coba Stack ---
history = InvestigationStack()
history.push_history("192.168.1.1 (Gateway)")
history.push_history("192.168.10.5 (Server Web)")
history.push_history("192.168.10.10 (Database)")

# Simulasi klik tombol 'Back'
history.pop_history()


# --- 3. Uji Coba Queue ---
incident_center = IncidentQueue()
incident_center.enqueue_incident("10.0.0.4 (PC Finansial)")
incident_center.enqueue_incident("10.0.0.9 (PC Direksi)")
incident_center.display_queue()

# Penanganan pertama
incident_center.dequeue_incident()
incident_center.display_queue()

