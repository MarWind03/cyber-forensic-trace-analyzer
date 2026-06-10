# =====================================================================
# ALGORITMA SORTING & SEARCHING
# =====================================================================

# 1. SORTING: Menggunakan Merge Sort (Efisien untuk Linked List/Array Besar - O(N log N))
# Mengurutkan objek LogEntry berdasarkan ukuran tingkat bahaya secara menurun (High -> Medium -> Low)
def merge_sort_logs(log_list):
    if len(log_list) <= 1:
        return log_list

    mid = len(log_list) // 2
    left_half = merge_sort_logs(log_list[:mid])
    right_half = merge_sort_logs(log_list[mid:])

    return _merge(left_half, right_half)

def _merge(left, right):
    result = []
    i = j = 0
    
    # Bobot nilai bahaya untuk perbandingan sorting
    severity_weights = {"High": 3, "Medium": 2, "Low": 1}

    while i < len(left) and j < len(right):
        # Ambil bobot severity dari objek LogEntry
        weight_left = severity_weights.get(left[i].severity, 0)
        weight_right = severity_weights.get(right[j].severity, 0)

        # Diurutkan secara descending (terbesar/terbahaya duluan)
        if weight_left >= weight_right:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


# 2. SEARCHING: Menggunakan Binary Search (O(log N))
# Syarat: Data log_list HARUS sudah terurut (misal diurutkan berdasarkan timestamp/activity)
# Di sini kita mencari log berdasarkan spesifik nama aktivitas pencurian data (Activity)
def linear_search_logs_by_activity(log_list, keyword):
    """
    Mencari log yang mengandung kata kunci (keyword) di mana saja dalam nama aktivitas.
    Mengembalikan LIST berisi semua log yang cocok (Multi-match).
    """
    hasil_pencarian = []
    keyword_lower = keyword.lower() # Case-insensitive
    
    # Linear Search menelusuri data dari awal sampai akhir satu per satu
    for log in log_list:
        # Operator 'in' mengecek apakah keyword ada di TENGGAH, AWAL, atau AKHIR kalimat
        if keyword_lower in log.activity.lower():
            hasil_pencarian.append(log)
            
    return hasil_pencarian
