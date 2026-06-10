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
