import json
import os
from src.models import LogEntry, Device, Server

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

    @staticmethod
    def load_network_assets(file_path):
        """Memuat data JSON dan mengonversinya menjadi objek OOP (Device/Server)"""
        
        asset_dict = {}
        if not os.path.exists(file_path): 
            return asset_dict
            
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                for item in data:
                    # Konversi list dari JSON menjadi Tuple untuk imutabilitas lokasi
                    loc_tuple = tuple(item['location'])
                    
                    if item['is_server']:
                        asset_dict[item['ip_address']] = Server(
                            item['ip_address'], item['mac_address'], 
                            loc_tuple, item['server_type']
                        )
                    else:
                        asset_dict[item['ip_address']] = Device(
                            item['ip_address'], item['mac_address'], loc_tuple
                        )
        except Exception as e:
            print(f"[!] Error membaca Aset JSON: {e}")
        return asset_dict

    @staticmethod
    def save_network_assets(file_path, asset_dict):
        """Mengonversi kembali objek OOP menjadi format tekstual JSON"""
        import json
        from src.models import Server
        
        data = []
        for ip, asset in asset_dict.items():
            is_server = isinstance(asset, Server)
            data.append({
                "ip_address": asset.ip_address,
                "mac_address": asset.mac_address,
                "location": list(asset.location), # Konversi kembali ke list untuk JSON
                "is_server": is_server,
                "server_type": asset.server_type if is_server else None
            })
            
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)