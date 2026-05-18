# 1. OOP
class Device:
    def __init__(self, ip_address, mac_address, location_tuple):
        self.ip_address = ip_address
        self.mac_address = mac_address
        self.location = location_tuple  # Menggunakan Tuple (Gedung, Lantai, Rak)
        self.status = "Normal"

    def display_info(self):
        return f"IP: {self.ip_address} | Lokasi: {self.location} | Status: {self.status}"

# Child Class khusus Server
class Server(Device):
    def __init__(self, ip_address, mac_address, location_tuple, server_type):
        super().__init__(ip_address, mac_address, location_tuple)
        self.server_type = server_type  # Contoh: "Database", "Web Server"
        self.critical_level = "High"

# Class untuk menampung satu baris data log
class LogEntry:
    def __init__(self, timestamp, source_ip, destination_ip, activity, severity):
        self.timestamp = timestamp
        self.source_ip = source_ip
        self.destination_ip = destination_ip
        self.activity = activity
        self.severity = severity  # "Low", "Medium", "High"

raw_logs_list = [
    LogEntry("2026-05-18 10:00:01", "192.168.10.50", "192.168.10.1", "Login Attempt", "Low"),
    LogEntry("2026-05-18 10:02:15", "185.220.101.5", "192.168.10.1", "SQL Injection", "High")
]


# 2. List, Tuple, Set, Dictionary

# TUPLE: Menyimpan koordinat fisik server yang TIDAK BOLEH BERUBAH (Immutable)
# Format: (Nama_Gedung, Lantai, Nomor_Rak)
location_server_A = ("Gedung_C", 1, "Meja-12")
location_pc_admin = ("Gedung_Rektorat", 3, "Rak-05")

# DICTIONARY: Menyimpan repositori semua perangkat (Key: IP Address, Value: Objek Device)
network_repository = {}

# Mengisi dictionary dengan objek OOP yang sudah dibuat
network_repository["192.168.10.1"] = Server("192.168.10.1", "00:1A:2B:3C:4D:5E", location_server_A, "Database")
network_repository["192.168.10.50"] = Device("192.168.10.50", "00:1A:2B:3C:4D:9F", location_pc_admin)

# SET: Menyimpan IP Blacklist secara unik (Mencegah Duplikasi)
blacklist_ips = {"185.220.101.5", "45.227.254.12"} 
blacklist_ips.add("185.220.101.5")  # Jika dimasukkan lagi, Set otomatis mengabaikannya

# LIST: Menyimpan antrean log mentah yang baru masuk secara urut
raw_logs_list = [
    LogEntry("2026-05-18 10:00:01", "192.168.10.50", "192.168.10.1", "Login Attempt", "Low"),
    LogEntry("2026-05-18 10:02:15", "185.220.101.5", "192.168.10.1", "SQL Injection", "High")
]
