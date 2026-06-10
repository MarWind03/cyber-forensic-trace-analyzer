class ThreatHashTable:
    def __init__(self, size=10):
        self.size = size
        # Membuat array of lists untuk penanganan kolisi (Chaining)
        self.table = [[] for _ in range(self.size)]

    def hash_function(self, key_ip):
        # Fungsi hash sederhana: menjumlahkan angka dari IP, lalu di-modulo 10
        # Contoh: "192.168.1.1" -> 192+168+1+1 = 362 % 10 = 2
        try:
            angka = map(int, key_ip.split('.'))
            return sum(angka) % self.size
        except ValueError:
            return sum(ord(char) for char in key_ip) % self.size

    def insert(self, ip_address, status_ancaman):
        index = self.hash_function(ip_address)
        
        # Cek apakah IP sudah ada di dalam bucket, jika ada update statusnya
        for item in self.table[index]:
            if item[0] == ip_address:
                item[1] = status_ancaman
                return
        
        # Jika belum ada, masukkan data baru (IP, Status) ke dalam bucket
        self.table[index].append([ip_address, status_ancaman])

    def search(self, ip_address):
        index = self.hash_function(ip_address)
        
        # Cari di dalam bucket berdasarkan index hash
        for item in self.table[index]:
            if item[0] == ip_address:
                return item[1]  # Mengembalikan status ancaman (e.g., "Dangerous")
        return "Clean / Unknown"  # Jika tidak ditemukan
    