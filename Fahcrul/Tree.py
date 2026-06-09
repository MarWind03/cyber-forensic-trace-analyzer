#Process Tree Malware
class ProcessNode:
    def __init__(self, process_name):
        self.process_name = process_name
        self.children = []

    def add_child(self, child_process):
        self.children.append(child_process)


explorer = ProcessNode("explorer.exe")
chrome = ProcessNode("chrome.exe")
updater = ProcessNode("updater.exe")
malware = ProcessNode("malware.exe")

explorer.add_child(chrome)
chrome.add_child(updater)
updater.add_child(malware)


#Rekrusif menampilkan tree
def display_process_tree(node, level=0):
    print("   " * level + node.process_name)

    for child in node.children:
        display_process_tree(child, level + 1)






#Rekursif mencari root penyebab infeksi dalam tree
def find_root_process(node):
    if node is None:
        return None

    if not hasattr(node, "parent"):
        return node

    if node.parent is None:
        return node

    return find_root_process(node.parent)
