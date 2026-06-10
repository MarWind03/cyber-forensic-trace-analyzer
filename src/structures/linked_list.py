class TaskNode:
    def __init__(self, task_description):
        self.task = task_description
        self.next = None  # Menunjuk ke tugas berikutnya

class InvestigationTodoList:
    def __init__(self):
        self.head = None

    # Tambah tugas baru di akhir daftar
    def add_task(self, task_description):
        new_node = TaskNode(task_description)
        if not self.head:
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    # Hapus tugas pertama (head) setelah selesai dikerjakan
    def complete_task(self):
        if not self.head:
            print("Semua tugas investigasi sudah selesai!")
            return None
        completed = self.head.task
        self.head = self.head.next  # Geser head ke tugas berikutnya
        return completed

    # Cetak semua rencana kerja
    def display_tasks(self):
        current = self.head
        if not current:
            print("Tidak ada tugas tersisa.")
            return
        print("\n--- RENCANA KERJA INVESTIGASI ---")
        while current:
            print(f"[ ] {current.task}")
            current = current.next

class LogNode:
    def __init__(self, log_obj):
        self.log = log_obj  # Menyimpan objek LogEntry dari Fase 1
        self.next = None    # Menunjuk log setelahnya
        self.prev = None    # Menunjuk log sebelumnya

class ChronologicalTimeline:
    def __init__(self):
        self.head = None
        self.tail = None

    # Menambahkan log baru di akhir timeline (terkini)
    def append_log(self, log_obj):
        new_node = LogNode(log_obj)
        if not self.head:
            self.head = new_node
            self.tail = new_node
            return
        self.tail.next = new_node
        new_node.prev = self.tail
        self.tail = new_node

    def explore_timeline(self):
        if not self.head:
            print("[!] Timeline log masih kosong.")
            return
        
        current = self.head
        while current:
            print("\n" + "="*40)
            print("         NAVIGASI TIMELINE LOG        ")
            print("="*40)
            print(f"Waktu    : {current.log.timestamp}")
            print(f"Sumber   : {current.log.source_ip}")
            print(f"Tujuan   : {current.log.destination_ip}")
            print(f"Aktivitas: {current.log.activity}")
            print(f"Bahaya   : {current.log.severity}")
            print("="*40)
            
            pilihan = input("[N]ext Log / [P]rev Log / [E]xit Menu: ").lower()
            if pilihan == 'n' and current.next:
                current = current.next
            elif pilihan == 'p' and current.prev:
                current = current.prev
            elif pilihan == 'e':
                break
            elif pilihan != 'n' and pilihan != 'p' and pilihan != 'e':
                print("\n[!] Input tidak valid!.")
            else:
                print("\n[!] Tidak ada log lebih lanjut di arah tersebut.")
    
class GuardNode:
    def __init__(self, server_ip):
        self.server_ip = server_ip
        self.next = None

class CircularServerGuard:
    def __init__(self):
        self.head = None
        self.tail = None

    # Menambahkan server ke dalam lingkaran rute patroli
    def add_to_patrol(self, server_ip):
        new_node = GuardNode(server_ip)
        if not self.head:
            self.head = new_node
            self.tail = new_node
            new_node.next = self.head  # Menunjuk ke dirinya sendiri (berputar)
            return
        
        self.tail.next = new_node
        self.tail = new_node
        self.tail.next = self.head  # Mengunci lingkaran kembali ke head

    # Simulasi patroli berputar (misal: berjalan 2 putaran penuh)
    def run_patrol_simulation(self, threat_table, incident_queue):
        if not self.head:
            print("[!] Rute patroli kosong. Daftarkan server terlebih dahulu.")
            return
        
        print("\n----- MEMULAI PATROLI OTOMATIS -----")
        current = self.head
        step = 1
        while True:
            status_ancaman = threat_table.search(current.server_ip)

            if "Clean" in status_ancaman or "Unknown" in status_ancaman:
                print(f"Patroli {step}: [{current.server_ip}] terpantau AMAN.")
                
            elif "Low" in status_ancaman:
                print(f"Patroli {step}: [{current.server_ip}] Anomali Ringan ({status_ancaman}).")
                
            elif "Medium" in status_ancaman:
                print(f"Patroli {step}: [{current.server_ip}] Peringatan Sedang ({status_ancaman}).")
                
            elif "High" in status_ancaman or "Kritis" in status_ancaman:
                print(f"Patroli {step}: BAHAYA KRITIS! [{current.server_ip}] berstatus: ({status_ancaman})!")
            
            current = current.next
            step += 1
            # Jika current kembali menunjuk ke head, putaran selesai!
            if current == self.head:
                print("[+] Satu siklus patroli jaringan telah selesai.")
                break