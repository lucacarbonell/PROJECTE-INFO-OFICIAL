class Node:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.neighbors = []  # Nodos vecinos directos

    def add_neighbor(self, neighbor_node):
        if neighbor_node not in self.neighbors:
            self.neighbors.append(neighbor_node)
            return True
        return False

    def __repr__(self):
        return f"Node('{self.name}', {self.x}, {self.y})"

def Distance(n1, n2):
    return ((n1.x - n2.x) ** 2 + (n1.y - n2.y) ** 2) ** 0.5