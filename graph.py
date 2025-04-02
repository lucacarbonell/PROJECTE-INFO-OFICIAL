from node import node
from segment import segment
import matplotlib.pyplot as plt
import math

class Graph:
    def __init__(self):
        self.nodes = []
        self.segments = []

    def AddNode(self, n: node):
        if any(existing_node.name == n.name for existing_node in self.nodes):
            return False
        self.nodes.append(n)
        return True

    def AddSegment(self, nameSegment, nameOriginNode, nameDestinationNode):
        origin = next((n for n in self.nodes if n.name == nameOriginNode), None)
        destination = next((n for n in self.nodes if n.name == nameDestinationNode), None)

        if origin and destination:
            seg = segment(nameSegment, origin, destination)
            self.segments.append(seg)
            origin.neighbors.append(destination)
            destination.neighbors.append(origin)
            return True
        return False

    def CalculateDistance(self, node1, node2):
        return round(math.sqrt((node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2), 2)

    def GetClosest(self, x, y):
        closest_node = None
        min_distance = float('inf')

        for n in self.nodes:
            dist = math.sqrt((n.x - x) ** 2 + (n.y - y) ** 2)
            if dist < min_distance:
                min_distance = dist
                closest_node = n

        return closest_node

    def Plot(self):
        fig, ax = plt.subplots()

        for n in self.nodes:
            ax.scatter(n.x, n.y, color='gray')
            ax.text(n.x, n.y, n.name, fontsize=12, verticalalignment='bottom')

        for seg in self.segments:
            x_values = [seg.origin.x, seg.destination.x]
            y_values = [seg.origin.y, seg.destination.y]
            ax.plot(x_values, y_values, 'k--')

            # Afegir el cost (distància) al centre del segment
            mid_x = (seg.origin.x + seg.destination.x) / 2
            mid_y = (seg.origin.y + seg.destination.y) / 2
            ax.text(mid_x, mid_y, f"{seg.cost:.2f}", fontsize=10, color='red')

        plt.xlabel("Coordenada X")
        plt.ylabel("Coordenada Y")
        plt.title("Espai Aeri")
        plt.show()

    def PlotNode(self, nameOrigin):
        node = next((n for n in self.nodes if n.name == nameOrigin), None)
        if not node:
            return False

        fig, ax = plt.subplots()

        for n in self.nodes:
            ax.scatter(n.x, n.y, color='gray')
            ax.text(n.x, n.y, n.name, fontsize=12, verticalalignment='bottom')

        ax.scatter(node.x, node.y, color='blue')

        for neighbor in node.neighbors:
            ax.scatter(neighbor.x, neighbor.y, color='green')
            ax.plot([node.x, neighbor.x], [node.y, neighbor.y], 'r-', linewidth=2)

            # Afegir el cost (distància) al centre del segment
            mid_x = (node.x + neighbor.x) / 2
            mid_y = (node.y + neighbor.y) / 2
            distance = self.CalculateDistance(node, neighbor)
            ax.text(mid_x, mid_y, f"{distance:.2f}", fontsize=10, color='red')

        plt.xlabel("X")
        plt.ylabel("Y")
        plt.title(f"Connections of {nameOrigin}")
        plt.show()

        return True


def CreateGraphFromFile(filename):
    G = Graph()

    with open(filename, 'r') as f:
        lines = f.readlines()

    # Llegim els nodes
    node_section = True
    for line in lines:
        line = line.strip()

        if line == "Segments:":
            node_section = False
            continue

        if node_section:
            # La línia és d'un node
            parts = line.split()
            if len(parts) == 3:
                name = parts[0]
                x = float(parts[1])
                y = float(parts[2])
                AddNode(G, node(name, x, y))
        else:
            # La línia és d'un segment
            parts = line.split()
            if len(parts) == 3:
                name_segment = parts[0]
                name_origin = parts[1]
                name_destination = parts[2]
                AddSegment(G, name_segment, name_origin, name_destination)

    return G


# Funcions globals per compatibilitat amb test_graph.py
def AddNode(G, n: node):
    return G.AddNode(n)

def AddSegment(G, nameSegment, nameOriginNode, nameDestinationNode):
    return G.AddSegment(nameSegment, nameOriginNode, nameDestinationNode)

def GetClosest(G, x, y):
    return G.GetClosest(x, y)

def Plot(G):
    return G.Plot()

def PlotNode(G, nameOrigin):
    return G.PlotNode(nameOrigin)
