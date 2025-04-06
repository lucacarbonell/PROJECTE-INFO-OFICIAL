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

    def AddNodeInteractive(self, x, y):
        """Afegir un node a les coordenades seleccionades per l'usuari"""
        node_name = f"Node{x}-{y}"
        new_node = node(node_name, x, y)
        self.AddNode(new_node)
        return new_node

    def AddSegmentInteractive(self, node1, node2):
        """Afegir un segment entre dos nodes seleccionats per l'usuari"""
        segment_name = f"Seg_{node1.name}_{node2.name}"
        self.AddSegment(segment_name, node1.name, node2.name)

    def RemoveNode(self, node_name):
        """Eliminar un node i els seus segments associats"""
        node_to_remove = next((n for n in self.nodes if n.name == node_name), None)
        if node_to_remove:
            # Eliminar els segments associats a aquest node
            self.segments = [s for s in self.segments if s.origin != node_to_remove and s.destination != node_to_remove]
            # Eliminar el node de la llista de nodes
            self.nodes.remove(node_to_remove)
            return True
        return False

    def SaveToFile(self, filename):
        """Guardar el gràfic en un fitxer de text amb el format indicat"""
        with open(filename, 'w') as file:
            file.write("Nodes:\n")
            for node in self.nodes:
                file.write(f"{node.name} {node.x} {node.y}\n")

            file.write("\nSegments:\n")
            for segment in self.segments:
                file.write(f"{segment.name} {segment.origin.name} {segment.destination.name}\n")

    def PlotNode(self, node_name):
        """Mostra un node específic i els seus veïns"""
        node = next((n for n in self.nodes if n.name == node_name), None)
        if not node:
            return False

        fig, ax = plt.subplots()
        ax.scatter(node.x, node.y, color='blue')
        ax.text(node.x, node.y, node.name, fontsize=12, verticalalignment='bottom')

        for neighbor in node.neighbors:
            ax.scatter(neighbor.x, neighbor.y, color='green')
            ax.plot([node.x, neighbor.x], [node.y, neighbor.y], 'r-', linewidth=2)

        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_title(f"Veïns de {node_name}")

        plt.show()

    def CreateGraphFromFile(self, file_path):
        """Crea un gràfic a partir d'un fitxer amb nodes i segments"""
        new_graph = Graph()
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                mode = None
                for line in lines:
                    line = line.strip()
                    if not line:  # Skip empty lines
                        continue

                    if line == "Nodes:":
                        mode = "nodes"
                        continue
                    elif line == "Segments:":
                        mode = "segments"
                        continue

                    parts = line.split()

                    if mode == "nodes" and len(parts) == 3:
                        # Format: A 1 20
                        AddNode(new_graph, node(parts[0], float(parts[1]), float(parts[2])))
                    elif mode == "segments" and len(parts) == 3:
                        # Format: AB A B
                        AddSegment(new_graph, parts[0], parts[1], parts[2])

        except FileNotFoundError:
            print(f"Error: El fitxer {file_path} no es troba.")
        return new_graph

    def DesignGraph(self):
        """Permet dissenyar un gràfic afegint nodes i segments interactivament."""
        self.nodes = []  # Reseteja els nodes
        self.segments = []  # Reseteja els segments

        print("Dissenya el gràfic. Fes clic per afegir nodes i segments.")
        # Esperem que el codi per interactuar amb Tkinter estigui implementat a la interfície per afegir nodes i segments
        # Aquesta funcionalitat es podria implementar a la interficie gràfica (vegeu els canvis a interface.py)

        return self

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
