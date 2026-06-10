import json
import os
from src.models import LogEntry

class CyberFileHandler:
    @staticmethod
    def load_logs_from_json(file_path):
        log_objects = []
        if not os.path.exists(file_path): return log_objects
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                for item in data:
                    log_objects.append(LogEntry(
                        item['timestamp'], item['source_ip'], 
                        item['destination_ip'], item['activity'], item['severity']
                    ))
        except Exception as e: print(f"[!] Error membaca LOG JSON: {e}")
        return log_objects

    @staticmethod
    def save_logs_to_json(file_path, log_list):
        data = [{"timestamp": l.timestamp, "source_ip": l.source_ip, "destination_ip": l.destination_ip, "activity": l.activity, "severity": l.severity} for l in log_list]
        with open(file_path, 'w') as file: json.dump(data, file, indent=4)

    # --- INPUT/OUTPUT DINAMIS BARU ---
    @staticmethod
    def load_simple_list(file_path):
        """Memuat list biasa dari JSON (Untuk Todo-List dan Patroli)"""
        if not os.path.exists(file_path): return []
        with open(file_path, 'r') as file: return json.load(file)

    @staticmethod
    def save_simple_list(file_path, data_list):
        """Menyimpan list biasa ke JSON"""
        with open(file_path, 'w') as file: json.dump(data_list, file, indent=4)

    @staticmethod
    def load_process_tree(file_path):
        """Memuat struktur flat Tree dari JSON"""
        if not os.path.exists(file_path): return []
        with open(file_path, 'r') as file: return json.load(file)

    @staticmethod
    def save_process_tree(file_path, flat_tree_data):
        """Menyimpan struktur flat Tree ke JSON"""
        with open(file_path, 'w') as file: json.dump(flat_tree_data, file, indent=4)

    @staticmethod
    def save_report(file_path, content):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file: file.write(content)