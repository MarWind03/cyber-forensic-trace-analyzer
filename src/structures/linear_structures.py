class Node:
    def __init__(self, ip_address):
        self.ip_address = ip_address
        self.next = None

class InvestigationStack:
    def __init__(self):
        self.head = Node("Command Center")  # Pointer ke node paling atas stack
        self.size = 0

    def push_history(self, ip_address):
        new_node = Node(ip_address)

        new_node.next = self.head
        self.head = new_node
        self.size += 1
        print(f"Membuka : {ip_address}")

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
        self.size -= 1
        print(f"Kembali dari {current_page} ke : {previous_page}")
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

    def get_current(self):
        if self.is_empty():
            return "Main Menu"
        return self.head.ip_address

class IncidentQueue:
    def __init__(self):
        self.front = None  # Pointer depan antrean
        self.rear = None   # Pointer belakang antrean
        self.size = 0

    # Masukkan server ke antrean (enqueue)
    def enqueue_incident(self, ip_address):
        new_node = Node(ip_address)

        # Jika antrean kosong
        if self.rear is None:
            self.front = self.rear = new_node
        else:
            # Sambungkan node baru ke belakang
            self.rear.next = new_node
            self.rear = new_node

        self.size += 1

        print(f"[ALERT] {ip_address} dimasukkan ke antrean penanganan bahaya!")

    # Keluarkan server dari antrean (dequeue)
    def dequeue_incident(self):
        if self.front is None:
            print("Aman! Tidak ada antrean insiden siber aktif.")
            return None

        handled_server = self.front.ip_address

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
            print(f"{index}. Urutan Penanganan -> {current.ip_address}")
            current = current.next
            index += 1

    def is_empty(self):
        return self.front is None

