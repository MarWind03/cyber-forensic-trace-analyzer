def bubble_sort_logs(log_list): 
    n = len(log_list)
    # Mengubah teks tanggal/waktu menjadi format yang bisa dibandingkan dengan lebih tepat.
    # Tapi karena format waktunya sudah YYYY-MM-DD, di bubble sort cukup dibandingkan sebagai string saja.
    
    for i in range(n):
        swapped = False
        for j in range(0, n-i-1):
            # Bandingkan timestamp string
            if log_list[j].timestamp > log_list[j+1].timestamp:
                # Tukar posisi
                log_list[j], log_list[j+1] = log_list[j+1], log_list[j]
                swapped = True
        if not swapped:
            break
    print("\n[SUCCESS] Log berhasil diurutkan secara kronologis (Bubble Sort).")

def binary_search_log(log_list, target_timestamp):
      
    low = 0
    high = len(log_list) - 1

    while low <= high:
        mid = (low + high) // 2
        mid_timestamp = log_list[mid].timestamp

        if mid_timestamp == target_timestamp:
            return log_list[mid] # Ketemu
        elif mid_timestamp < target_timestamp:
            low = mid + 1 # Cari di kanan (waktu lebih besar)
        else:
            high = mid - 1 # Cari di kiri (waktu lebih kecil)
    
    return None # Tidak ketemu

    if mid_timestamp == target_timestamp:
            return log_list[mid] # Ketemu
    elif mid_timestamp < target_timestamp:
            low = mid + 1 # Cari di kanan (waktu lebih besar)
    else:
            high = mid - 1 # Cari di kiri (waktu lebih kecil)
    
    return None # Tidak ketemu