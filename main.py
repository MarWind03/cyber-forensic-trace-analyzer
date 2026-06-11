import os
import time
from src.models import LogEntry, Device, Server
from src.file_handler import CyberFileHandler
from src.algorithms import merge_sort_logs, linear_search_logs_by_activity

from src.structures.linked_list import InvestigationTodoList, ChronologicalTimeline, CircularServerGuard
from src.structures.linear_structures import InvestigationStack, IncidentQueue
from src.structures.trees_graphs import ProcessTree, NetworkGraph
from src.structures.hash_table import ThreatHashTable

class CyberTraceApp:
    def __init__(self):
        # Path File Database JSON
        self.log_path = os.path.join("data", "network_logs.json")
        self.todo_path = os.path.join("data", "todo_tasks.json")
        self.patrol_path = os.path.join("data", "patrol_servers.json")
        self.tree_path = os.path.join("data", "process_tree.json")
        self.report_path = os.path.join("reports", "cyber_report.txt")
        self.asset_path = os.path.join("data", "network_assets.json")
        
        # State Data di Memori (Python List / Set biasa untuk backup simpan JSON)
        self.raw_logs = []
        self.raw_todos = []
        self.raw_patrols = []
        self.raw_processes = []
        self.blacklist_ips = set()
        self.network_inventory = CyberFileHandler.load_network_assets(self.asset_path)
        
        
        # Inisialisasi Objek Struktur Data Murni Pointer
        self.timeline = ChronologicalTimeline()
        self.incident_queue = IncidentQueue()
        self.net_graph = NetworkGraph()
        self.threat_table = ThreatHashTable(10)
        self.todo_list = InvestigationTodoList()
        self.guard = CircularServerGuard()
        self.history = InvestigationStack()
        self.proc_tree = None # Akan dibentuk dinamis dari JSON

    def sync_log_data(self, log):
        """Menyebarkan 1 objek log ke seluruh struktur data terkait"""
        self.raw_logs.append(log)
        self.timeline.append_log(log)
        self.net_graph.add_traffic_edge(log.source_ip, log.destination_ip)
        self.threat_table.insert(log.destination_ip, f"[{log.severity}] {log.activity} dari {log.source_ip}")

        if log.severity.lower() == "high":
            self.incident_queue.enqueue_incident(log.destination_ip)
            self.threat_table.insert(log.source_ip, f"Kritis: Attacker Node")
            self.blacklist_ips.add(log.source_ip)

    def load_initial_data(self):
        """Fungsi booting untuk membangun ulang semua struktur data dari file JSON"""
        print("[+] Sinkronisasi database JSON ke struktur data memori...")
        time.sleep(1)
        
        # 1. Load Logs
        logs = CyberFileHandler.load_logs_from_json(self.log_path)
        for log in logs:
            self.sync_log_data(log)
        
        # 2. Load Todo-List (Single LL)
        self.raw_todos = CyberFileHandler.load_simple_list(self.todo_path)
        for task in self.raw_todos:
            self.todo_list.add_task(task)
            
        # 3. Load Patrol Targets (Circular LL)
        self.raw_patrols = CyberFileHandler.load_simple_list(self.patrol_path)
        for server in self.raw_patrols:
            self.guard.add_to_patrol(server)
            
        # 4. Load Process Tree (Membangun objek Tree dari JSON)
        self.raw_processes = CyberFileHandler.load_process_tree(self.tree_path)
        if self.raw_processes:
            # Cari root node (yang parent_pid-nya null)
            root_data = next((p for p in self.raw_processes if p['parent_pid'] is None), None)
            if root_data:
                self.proc_tree = ProcessTree(root_data['name'], root_data['pid'])
                
                # Masukkan sisa node anak secara bertahap
                inserted_count = 0
                while inserted_count < len(self.raw_processes) - 1:
                    for p in self.raw_processes:
                        if p['parent_pid'] is not None:
                            # Coba insert, jika sukses berarti parent sudah ada di Tree
                            if self.proc_tree.insert_process(p['parent_pid'], p['name'], p['pid']):
                                inserted_count += 1

    def run(self):
        self.load_initial_data()
        
        while True:
            print("\n" + "="*50)
            print("        CYBER TRACE - COMMAND CENTER        ")
            print("="*50)
            print(" [1] Tambah Log Insiden")
            print(" [2] Navigasi Kronologi Waktu")
            print(" [3] Penanganan Antrean Insiden")
            print(" [4] Lacak Rute Sebaran Infeksi Jaringan")
            print(" [5] Kelola & Lacak Pohon Proses Server")
            print(" [6] Cari Aktivitas Log")
            print(" [7] Urutkan Log Paling Kritis")
            print(" [8] Cek Status Keamanan IP")
            print(" [9] Manajemen Tugas & Rute Patroli")
            print(" [10] Ekspor Laporan Akhir & Matikan Sistem")
            print("="*50)
            
            pilihan = input("Pilih Modul (1-10): ")

            if pilihan == "1":
                print("\n--- INPUT DATA LOG BARU ---")
                waktu = input("Timestamp (e.g., yy-mm-dd 10:00:19): ")
                src = input("Masukkan Source IP (Penyerang): ")
                dst = input("Masukkan Destination IP (Korban): ")
                act = input("Aktivitas (e.g., Ransomware Run): ")
                print("Pilih Tingkat Bahaya (Severity):")
                print(" [1] Low\n [2] Medium\n [3] High")
                sev_pilihan = input("Pilih (1/2/3): ")
                if sev_pilihan == "1":
                    sev = "Low"
                elif sev_pilihan == "2":
                    sev = "Medium"
                elif sev_pilihan == "3":
                    sev = "High"
                else:
                    print("[!] ERROR: Pilihan Severity tidak dikenali. Input dibatalkan.")
                    continue
                
                log_baru = LogEntry(waktu, src, dst, act, sev.capitalize())
                self.sync_log_data(log_baru) 
                CyberFileHandler.save_logs_to_json(self.log_path, self.raw_logs)
                print("[+] Log berhasil disimpan ke database JSON dan disinkronkan!")

            elif pilihan == "2":
                self.history.push_history("Timeline Menu")
                self.timeline.explore_timeline()
                self.history.pop_history()

            elif pilihan == "3":
                self.history.push_history("Incident Center")
                print("\n--- PUSAT PENANGANAN INSIDEN  ---")
                print(" [1] Lihat Antrean & Tangani Insiden")
                print(" [2] Tambah IP ke Antrean Manual ")
                sub_q = input("Pilih aksi (1/2): ")

                if sub_q == "1":
                    self.incident_queue.display_queue()
                    if not self.incident_queue.is_empty():
                        sub_sub = input("\nTangani insiden terdepan sekarang? (y/n): ").lower()
                        if sub_sub == 'y':
                            target = self.incident_queue.dequeue_incident()
                            print(f"[+] Sukses membersihkan ancaman di perangkat: {target}")
                            self.threat_table.insert(target, "[Clean] Selesai Diinvestigasi")
                        elif sub_sub != 'n':
                            print("[!] Pilihan tidak valid.")
                            
                elif sub_q == "2":
                    ip_baru = input("Masukkan IP perangkat yang terinfeksi: ")
                    self.incident_queue.enqueue_incident(ip_baru)
                    self.threat_table.insert(ip_baru, "[High] Dicurigai (Input Manual Detektif)")
                    print(f"[+] Perangkat {ip_baru} berhasil ditambahkan ke antrean darurat!")
                
                else:
                    print("[!] Pilihan tidak valid.")

                self.history.pop_history()

            elif pilihan == "4":
                self.history.push_history("Network Graph Mapper")

                print("\n--- PETA PERGERAKAN INFEKSI JARINGAN ---")
                self.net_graph.display_network_graph()

                target_ip = input("\nMasukkan IP Node asal untuk melacak lompatan terjauh: ")
                if target_ip not in self.net_graph.adjacency_list:
                    print(f"[!] Node IP {target_ip} tidak pernah tercatat melakukan aktivitas di Graph.")
                else:
                    rute = self.net_graph.trace_infection_path_recursive(target_ip)
                    print(f"[Hasil Analisis]: {' -> '.join(rute) if rute else 'IP tidak ditemukan'}")
                self.history.pop_history()

            elif pilihan == "5":
                self.history.push_history("Process Tree Manager")
                print("\n--- MANAJEMEN POHON PROSES ---")
                if self.proc_tree:
                    self.proc_tree.display_tree_recursive(self.proc_tree.root)
                else:
                    print("[!] Pohon proses belum terbentuk.")
                
                print("\nMenu: [1] Tambah Proses Baru | [2] Lacak Akar Masalah (Root Cause) | [3] Kembali")
                sub = input("Pilih tindakan: ")
                
                if sub == "1":
                    try:
                        p_pid = int(input("Masukkan PID Induk (Parent PID): "))
                        c_name = input("Masukkan Nama Proses Baru: ")
                        c_pid = int(input("Masukkan PID Proses Baru: "))
                        
                        if self.proc_tree.insert_process(p_pid, c_name, c_pid):
                            self.raw_processes.append({"pid": c_pid, "name": c_name, "parent_pid": p_pid})
                            CyberFileHandler.save_process_tree(self.tree_path, self.raw_processes)
                            print("[+] Proses baru berhasil diinjeksikan ke Tree dan JSON!")
                        else:
                            print("[!] Gagal! Parent PID tidak ditemukan.")
                    except ValueError:
                        print("[!] FORMAT ERROR: PID hanya boleh menggunakan angka.")
                        
                elif sub == "2":
                    try:
                        pid = int(input("Masukkan PID aplikasi mencurigakan untuk dilacak: "))
                        rute = self.proc_tree.trace_root_cause_recursive(self.proc_tree.root, pid)
                        print(f"[Hasil Lacak]: {' -> '.join(rute) if rute else 'PID tidak ditemukan'}")
                    except ValueError:
                        print("[!] FORMAT ERROR: PID hanya boleh menggunakan angka.")
                
                else:
                    print("[!] Pilihan tidak valid.")

                self.history.pop_history()

            elif pilihan == "6":
                target = input("\nMasukkan kata kunci aktivitas yang dicari (e.g., 'scan' atau 'force'): ")
                
                hasil = linear_search_logs_by_activity(self.raw_logs, target)
                
                if hasil:
                    print(f"\n[DITEMUKAN] Ada {len(hasil)} log yang mengandung kata '{target}':")
                    for log in hasil:
                        print(f" -> {log.timestamp} | {log.source_ip} | [{log.severity}] {log.activity}")
                else:
                    print(f"[-] Tidak ada aktivitas log yang mengandung kata '{target}'.")

            elif pilihan == "7":
                sorted_logs = merge_sort_logs(self.raw_logs)
                print("\n--- URUTAN LOG BERDASARKAN TINGKAT BAHAYA  ---")
                for log in sorted_logs:
                    print(f" [{log.severity}] {log.timestamp} - {log.source_ip} -> {log.activity}")

            elif pilihan == "8":
                self.history.push_history("Threat & Asset Inspector")
                print("\n--- PUSAT INSPEKSI KEAMANAN & MANAJEMEN ASET ---")
                print(" [1] Inspeksi Keamanan & Deteksi Aset IP")
                print(" [2] Registrasi Perangkat Baru ke Inventaris")
                print(" [3] Kembali ke Menu Utama")
                sub_menu = input("Pilih tindakan (1/2/3): ").strip()
                if sub_menu == "1":
                    print("\n--- SUBSISTEM INSPEKSI INTEGRITAS IP ---")
                    ip = input("Masukkan IP Address sasaran inspeksi: ")
                    print(f"Status di Set Blacklist : {'TERBLOKIR (DANGEROUS)' if ip in self.blacklist_ips else 'CLEAN'}")
                    print(f"Informasi Hash Table    : {self.threat_table.search(ip)}")

                    print("-" * 50)
                    print("HASIL PELACAKAN ASET FISIK PERANGKAT: ")
                    if ip in self.network_inventory:
                        asset = self.network_inventory[ip]
                        # Memanggil fungsi dasar display_info dari Parent Class (Device)
                        print(f" Informasi Dasar : {asset.display_info()}")
                        
                        # Memeriksa secara dinamis apakah objek ini merupakan Child Class (Server)
                        if isinstance(asset, Server):
                            print(f" [!] Peringatan  : Perangkat ini merupakan INFRASTRUKTUR KRITIS!")
                            print(f" Tipe Layanan    : {asset.server_type} Server")
                            print(f" Level Proteksi  : {asset.critical_level}")
                    else:
                        print(" [?] Status Aset : Perangkat Luar Jaringan / Tidak Terdaftar di Inventaris.")
                    print("-" * 50)
                elif sub_menu == "2":
                    print("\n--- FORM REGISTRASI PERANGKAT JARINGAN BARU ---")
                    ip = input("Masukkan IP Address Baru   : ").strip()
                    mac = input("Masukkan MAC Address Baru  : ").strip()
                    
                    print("Koordinat Lokasi Fisik:")
                    gedung = input("  Nama Gedung/Sektor : ").strip()
                    lantai = input("  Lantai/Ruang       : ").strip()
                    rak    = input("  Nomor Rak/Posisi   : ").strip()
                    loc_tuple = (gedung, lantai, rak) # Membentuk struktur Tuple
                    
                    is_server_input = input("Apakah perangkat ini bertindak sebagai Server? (y/n): ").lower()
                    
                    if is_server_input == 'y':
                        server_type = input("Masukkan Jenis Layanan Server (e.g., Web/Database): ").strip()
                        # Instansiasi objek menggunakan Child Class
                        self.network_inventory[ip] = Server(ip, mac, loc_tuple, server_type)
                    elif is_server_input == 'n':
                        # Instansiasi objek menggunakan Parent Class
                        self.network_inventory[ip] = Device(ip, mac, loc_tuple)
                    else:
                        print("[!] Pilihan tidak valid.")

                    # Sinkronisasikan state memori RAM ke file penyimpanan fisik JSON
                    CyberFileHandler.save_network_assets(self.asset_path, self.network_inventory)
                    print(f"\n[+] BERHASIL: Perangkat [{ip}] resmi terdaftar dalam infrastruktur jaringan!")

                elif sub_menu != '3':
                    print("[!] Pilihan tidak valid.")
                self.history.pop_history()

            elif pilihan == "9":
                self.history.push_history("Task & Patrol Manager")
                print("\n--- PANEL MANAJEMEN TUGAS DAN PATROLI ---")
                print(" [A] Kelola Rencana Kerja ")
                print(" [B] Kelola & Jalankan Rute Patroli ")
                opsi = input("Pilih opsi (A/B): ").upper()
                
                if opsi == 'A':
                    self.todo_list.display_tasks()
                    print("\nAksi: [1] Tambah Tugas Baru | [2] Selesaikan Tugas Terdepan | [3] Kembali")
                    sub_t = input("Pilih: ")
                    if sub_t == "1":
                        t_baru = input("Ketik deskripsi tugas baru: ")
                        self.todo_list.add_task(t_baru)
                        self.raw_todos.append(t_baru)
                        CyberFileHandler.save_simple_list(self.todo_path, self.raw_todos)
                        print("[+] Tugas disimpan ke Todo-List dan JSON!")
                    elif sub_t == "2":
                        selesai = self.todo_list.complete_task()
                        if selesai:
                            self.raw_todos.remove(selesai)
                            CyberFileHandler.save_simple_list(self.todo_path, self.raw_todos)
                            print(f"[+] Sukses Menyelesaikan: {selesai}")
                    elif sub_t != "3":
                        print("[!] Pilihan tidak valid.")
                            
                elif opsi == 'B':
                    print("\nTarget Server Terdaftar:")
                    for s in self.raw_patrols: print(f" -> {s}")
                    print("\nAksi: [1] Tambah Server ke Rute | [2] Jalankan Simulasi Patroli | [3] Kembali")
                    sub_p = input("Pilih: ")
                    if sub_p == "1":
                        s_baru = input("Masukkan IP Server Baru: ")
                        self.guard.add_to_patrol(s_baru)
                        self.raw_patrols.append(s_baru)
                        CyberFileHandler.save_simple_list(self.patrol_path, self.raw_patrols)
                        print("[+] Server baru berhasil dikunci ke rute melingkar dan JSON!")
                    elif sub_p == "2":
                        self.guard.run_patrol_simulation(self.threat_table, self.incident_queue)
                    elif sub_p != "3":
                        print("[!] Pilihan tidak valid.")

                else:
                    print("[!] Pilihan tidak valid.")
                
                self.history.pop_history()


            elif pilihan == "10":
                laporan = (
                    f"==================================================\n"
                    f"       LAPORAN AKHIR FORENSIK: CYBER TRACE        \n"
                    f"==================================================\n"
                    f" Total Rekaman Log Masuk : {len(self.raw_logs)} baris\n"
                    f" Jumlah IP Ter-blacklist : {len(self.blacklist_ips)} perangkat\n"
                    f" Daftar Blacklist IP     : {list(self.blacklist_ips)}\n"
                    f" Status Akhir Keamanan   : INVESTIGASI SELESAI & DATABASE TERKUNCI\n"
                )
                CyberFileHandler.save_report(self.report_path, laporan)
                print("[+] Berhasil mengekspor 'reports/cyber_report.txt'. Mematikan sistem. Sampai jumpa!")
                break
            else:
                print("[!] Pilihan menu salah. Masukkan angka 1 sampai 10.")


if __name__ == "__main__":
    app = CyberTraceApp()
    app.run()
    