class Node:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.neighbors = []

def AddNeighbor(n1, n2):
    if n2 in n1.neighbors:
        return False
    n1.neighbors.append(n2)
    return True

def Distance(n1, n2):
    return ((n1.x - n2.x)**2 + (n1.y - n2.y)**2)**0.5
