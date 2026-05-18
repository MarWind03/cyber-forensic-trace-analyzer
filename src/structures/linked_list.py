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

    # Helper untuk demonstrasi navigasi di menu utama nanti
    def get_head(self):
        return self.head
    
# --- 1. Uji Coba Single Linked List ---
todo_list = InvestigationTodoList()
todo_list.add_task("Analisis Log Firewall")
todo_list.add_task("Isolasi Database Server")
todo_list.display_tasks()

print(f"\nSelesai mengerjakan: {todo_list.complete_task()}")
todo_list.display_tasks()