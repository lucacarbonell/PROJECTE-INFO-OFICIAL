from collections import deque
from node import Node
from segment import Segment
import matplotlib.pyplot as plt
from matplotlib.patches import Arrow


class Graph:
    def __init__(self):
        self.nodes = []
        self.segments = []

    def find_path_bfs(self, start_name, end_name):
        """Implementación correcta de BFS dentro de la clase Graph"""
        # Encontrar nodos de inicio y fin
        start = next((n for n in self.nodes if n.name == start_name), None)
        end = next((n for n in self.nodes if n.name == end_name), None)

        if not start or not end:
            return None

        # BFS para encontrar cualquier camino
        queue = deque()
        queue.append([start])
        visited = set([start])

        while queue:
            path = queue.popleft()
            node = path[-1]

            if node == end:
                return path

            for neighbor in node.neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append(new_path)

        # Si no hay camino directo, retorna None o un camino alternativo
        return None

    def plot_with_arrows(self):
        plt.figure(figsize=(10, 8))

        # Dibujar nodos
        for node in self.nodes:
            plt.plot(node.x, node.y, 'o', markersize=10, label=node.name)
            plt.text(node.x, node.y + 0.3, node.name, ha='center')

        # Dibujar segmentos con flechas
        for seg in self.segments:
            dx = seg.destination.x - seg.origin.x
            dy = seg.destination.y - seg.origin.y
            plt.arrow(seg.origin.x, seg.origin.y,
                      dx * 0.9, dy * 0.9,  # Acortar flecha para que no sobresalga
                      head_width=0.3, head_length=0.4,
                      fc='blue', ec='blue', length_includes_head=True)

            # Mostrar costo
            mid_x = (seg.origin.x + seg.destination.x) / 2
            mid_y = (seg.origin.y + seg.destination.y) / 2
            plt.text(mid_x, mid_y, f"{seg.cost:.1f}",
                     bbox=dict(facecolor='white', alpha=0.8))

        plt.grid(True)
        plt.axis('equal')
        plt.legend()
        plt.show()