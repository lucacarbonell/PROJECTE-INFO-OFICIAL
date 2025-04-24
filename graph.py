import matplotlib.pyplot as plt
from node import Node
from segment import Segment


class Graph:
    def __init__(self):
        self.nodes = []
        self.segments = []


def AddNode(g, n):
    if n in g.nodes:
        return False
    g.nodes.append(n)
    return True


def AddSegment(g, name, nameOrigin, nameDestination):
    origin = None
    destination = None

    for node in g.nodes:
        if node.name == nameOrigin:
            origin = node
        if node.name == nameDestination:
            destination = node

    if origin is None or destination is None:
        return False

    segment = Segment(name, origin, destination)
    g.segments.append(segment)

    # Añadir vecino
    origin.neighbors.append(destination)

    return True


def GetClosest(g, x, y):
    closest_node = None
    min_distance = float('inf')

    for node in g.nodes:
        distance = ((node.x - x) ** 2 + (node.y - y) ** 2) ** 0.5
        if distance < min_distance:
            min_distance = distance
            closest_node = node

    return closest_node


def Plot(g):
    plt.figure(figsize=(10, 8))

    # Dibujar segmentos
    for seg in g.segments:
        plt.plot([seg.origin.x, seg.destination.x],
                 [seg.origin.y, seg.destination.y],
                 'k-', linewidth=1)
        # Mostrar costo en el medio del segmento
        mid_x = (seg.origin.x + seg.destination.x) / 2
        mid_y = (seg.origin.y + seg.destination.y) / 2
        plt.text(mid_x, mid_y, f"{seg.cost:.1f}",
                 fontsize=8, ha='center', va='center',
                 bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))

    # Dibujar nodos
    for node in g.nodes:
        plt.plot(node.x, node.y, 'ko', markersize=10)
        plt.text(node.x, node.y, node.name,
                 fontsize=12, ha='center', va='center', color='white')

    plt.grid(True)
    plt.title("Graph Visualization")
    plt.show()


def PlotNode(g, nameOrigin):
    origin = None
    for node in g.nodes:
        if node.name == nameOrigin:
            origin = node
            break

    if origin is None:
        return False

    plt.figure(figsize=(10, 8))

    # Dibujar todos los segmentos en gris primero
    for seg in g.segments:
        plt.plot([seg.origin.x, seg.destination.x],
                 [seg.origin.y, seg.destination.y],
                 'gray', linewidth=1, alpha=0.3)

    # Resaltar segmentos conectados al nodo origen
    for seg in g.segments:
        if seg.origin == origin:
            plt.plot([seg.origin.x, seg.destination.x],
                     [seg.origin.y, seg.destination.y],
                     'r-', linewidth=2)
            # Mostrar costo en rojo
            mid_x = (seg.origin.x + seg.destination.x) / 2
            mid_y = (seg.origin.y + seg.destination.y) / 2
            plt.text(mid_x, mid_y, f"{seg.cost:.1f}",
                     fontsize=8, ha='center', va='center', color='red',
                     bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))

    # Dibujar nodos
    for node in g.nodes:
        if node == origin:
            color = 'blue'
        elif node in origin.neighbors:
            color = 'green'
        else:
            color = 'gray'

        plt.plot(node.x, node.y, 'o', markersize=10, color=color)
        plt.text(node.x, node.y, node.name,
                 fontsize=12, ha='center', va='center', color='white')

    plt.grid(True)
    plt.title(f"Neighbors of Node {nameOrigin}")
    plt.show()
    return True


# Añadir esto al final de graph.py (antes de las funciones de carga/guardado)

def CreateGraph_1():
    G = Graph()
    AddNode(G, Node("A", 1, 20))
    AddNode(G, Node("B", 8, 17))
    AddNode(G, Node("C", 15, 20))
    AddNode(G, Node("D", 18, 15))
    AddNode(G, Node("E", 2, 4))
    AddNode(G, Node("F", 6, 5))
    AddNode(G, Node("G", 12, 12))
    AddNode(G, Node("H", 10, 3))
    AddNode(G, Node("I", 19, 1))
    AddNode(G, Node("J", 13, 5))
    AddNode(G, Node("K", 3, 15))
    AddNode(G, Node("L", 4, 10))

    AddSegment(G, "AB", "A", "B")
    AddSegment(G, "AE", "A", "E")
    AddSegment(G, "AK", "A", "K")
    AddSegment(G, "BA", "B", "A")
    AddSegment(G, "BC", "B", "C")
    AddSegment(G, "BF", "B", "F")
    AddSegment(G, "BK", "B", "K")
    AddSegment(G, "BG", "B", "G")
    AddSegment(G, "CD", "C", "D")
    AddSegment(G, "CG", "C", "G")
    AddSegment(G, "DG", "D", "G")
    AddSegment(G, "DH", "D", "H")
    AddSegment(G, "DI", "D", "I")
    AddSegment(G, "EF", "E", "F")
    AddSegment(G, "FL", "F", "L")
    AddSegment(G, "GB", "G", "B")
    AddSegment(G, "GF", "G", "F")
    AddSegment(G, "GH", "G", "H")
    AddSegment(G, "ID", "I", "D")
    AddSegment(G, "IJ", "I", "J")
    AddSegment(G, "JI", "J", "I")
    AddSegment(G, "KA", "K", "A")
    AddSegment(G, "KL", "K", "L")
    AddSegment(G, "LK", "L", "K")
    AddSegment(G, "LF", "L", "F")

    return G


def CreateGraph_2():
    G = Graph()
    AddNode(G, Node("X", 5, 15))
    AddNode(G, Node("Y", 10, 10))
    AddNode(G, Node("Z", 15, 5))
    AddNode(G, Node("W", 20, 20))

    AddSegment(G, "XY", "X", "Y")
    AddSegment(G, "XZ", "X", "Z")
    AddSegment(G, "YW", "Y", "W")
    AddSegment(G, "ZW", "Z", "W")
    AddSegment(G, "YX", "Y", "X")
    AddSegment(G, "ZX", "Z", "X")

    return G
def LoadGraphFromFile(filename):
    g = Graph()

    try:
        with open(filename, 'r') as file:
            lines = file.readlines()

        # Primero creamos los nodos
        for line in lines:
            if line.startswith('NODE'):
                parts = line.strip().split(',')
                name = parts[1]
                x = float(parts[2])
                y = float(parts[3])
                AddNode(g, Node(name, x, y))

        # Luego creamos los segmentos
        for line in lines:
            if line.startswith('SEGMENT'):
                parts = line.strip().split(',')
                name = parts[1]
                origin = parts[2]
                destination = parts[3]
                AddSegment(g, name, origin, destination)

    except Exception as e:
        print(f"Error loading graph from file: {e}")
        return None

    return g


def SaveGraphToFile(g, filename):
    try:
        with open(filename, 'w') as file:
            # Escribir nodos
            for node in g.nodes:
                file.write(f"NODE,{node.name},{node.x},{node.y}\n")

            # Escribir segmentos
            for seg in g.segments:
                file.write(f"SEGMENT,{seg.name},{seg.origin.name},{seg.destination.name}\n")

    except Exception as e:
        print(f"Error saving graph to file: {e}")
        return False

    return True


from path import *


def FindShortestPath(g, origin_name, destination_name):
    # Encontrar nodos de origen y destino
    origin = None
    destination = None
    for node in g.nodes:
        if node.name == origin_name:
            origin = node
        if node.name == destination_name:
            destination = node

    if origin is None or destination is None:
        return None

    # Implementación del algoritmo A*
    open_paths = [Path([origin], 0)]

    while open_paths:
        # Encontrar el camino con el menor costo estimado
        current_path = min(open_paths, key=lambda p: p.cost + Distance(p.nodes[-1], destination))
        open_paths.remove(current_path)

        last_node = current_path.nodes[-1]

        # Si hemos llegado al destino
        if last_node == destination:
            return current_path

        # Expandir a los vecinos
        for neighbor in last_node.neighbors:
            if not ContainsNode(current_path, neighbor):
                # Encontrar el segmento correspondiente
                segment = None
                for seg in g.segments:
                    if seg.origin == last_node and seg.destination == neighbor:
                        segment = seg
                        break

                if segment:
                    new_path = AddNodeToPath(current_path, neighbor, segment.cost)
                    open_paths.append(new_path)


    return None  # No se encontró camino