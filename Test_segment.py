from node import Node
from segment import Segment
from graph import Graph  # Importa Graph en lugar de funciones sueltas


def test_graph_system():
    # Crear grafo
    g = Graph()

    # Crear y añadir nodos
    n1 = Node('A', 1, 1)
    n2 = Node('B', 4, 5)
    n3 = Node('C', 8, 2)
    n4 = Node('D', 5, 2)
    g.nodes.extend([n1, n2, n3, n4])

    # Crear y añadir segmentos
    seg1 = Segment('AB', n1, n2)
    seg2 = Segment('BC', n2, n3)
    seg3 = Segment('AD', n1, n4)
    seg4 = Segment('DC', n4, n3)
    g.segments.extend([seg1, seg2, seg3, seg4])

    # Establecer vecinos
    n1.add_neighbor(n2)
    n1.add_neighbor(n4)
    n2.add_neighbor(n3)
    n4.add_neighbor(n3)

    # 1. Buscar camino usando el método del grafo
    path = g.find_path_bfs('A', 'C')  # Ahora se llama desde la instancia g

    if path:
        print("\nCamino encontrado A -> C:")
        print(" → ".join([n.name for n in path]))
    else:
        print("\nNo se encontró camino directo")

    # 2. Visualizar
    g.plot_with_arrows()


if __name__ == "__main__":
    test_graph_system()