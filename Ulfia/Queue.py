class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class IncidentQueue:
    def __init__(self):
        self.front = None
        self.rear = None
        self.count = 0

    def enqueue(self, log_entry):
        """Masukkan log ke antrean jika severity-nya HIGH"""
        new_node = Node(log_entry)
        
        if self.rear is None:
            self.front = self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node
        self.count += 1

    def dequeue(self):
        """Keluarkan log untuk ditangani (FIFO)"""
        if self.front is None:
            return None
        
        temp = self.front
        self.front = temp.next
        
        if self.front is None:
            self.rear = None
        
        self.count -= 1
        return temp.data

    def display_queue(self):
        current = self.front
        if not current:
            print("\n[QUEUE] Antrean Insiden KOSONG.")
            return