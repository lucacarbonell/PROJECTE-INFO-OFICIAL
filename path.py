class Path:
    def __init__(self, nodes=None, cost=0):
        self.nodes = nodes if nodes is not None else []
        self.cost = cost

    def __repr__(self):
        return f"Path(nodes={[n.name for n in self.nodes]}, cost={self.cost})"


def AddNodeToPath(path, node, cost):
    new_path = Path(path.nodes.copy(), path.cost)
    new_path.nodes.append(node)
    new_path.cost += cost
    return new_path


def ContainsNode(path, node):
    return node in path.nodes


def CostToNode(path, node):
    if not ContainsNode(path, node):
        return -1
    # Simulamos el costo hasta el nodo (en una implementación real deberíamos calcularlo)
    return path.cost  # Esto es una simplificación


def PlotPath(graph, path):
    if not path.nodes:
        return

    plt.figure(figsize=(10, 8))

    # Dibujar todos los nodos y segmentos en gris
    for seg in graph.segments:
        plt.plot([seg.origin.x, seg.destination.x],
                 [seg.origin.y, seg.destination.y],
                 'gray', linewidth=1, alpha=0.3)

    # Dibujar nodos
    for node in graph.nodes:
        plt.plot(node.x, node.y, 'ko', markersize=8)
        plt.text(node.x, node.y, node.name,
                 fontsize=10, ha='center', va='center', color='white')

    # Dibujar el camino en rojo
    for i in range(len(path.nodes) - 1):
        origin = path.nodes[i]
        destination = path.nodes[i + 1]

        # Buscar el segmento correspondiente
        segment = None
        for seg in graph.segments:
            if seg.origin == origin and seg.destination == destination:
                segment = seg
                break

        if segment:
            plt.plot([origin.x, destination.x],
                     [origin.y, destination.y],
                     'r-', linewidth=2)
            # Mostrar costo
            mid_x = (origin.x + destination.x) / 2
            mid_y = (origin.y + destination.y) / 2
            plt.text(mid_x, mid_y, f"{segment.cost:.1f}",
                     fontsize=8, ha='center', va='center', color='red',
                     bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))

    # Resaltar nodos del camino
    for node in path.nodes:
        plt.plot(node.x, node.y, 'bo', markersize=10)

    plt.grid(True)
    plt.title(f"Shortest Path (Total cost: {path.cost:.2f})")
    plt.show()