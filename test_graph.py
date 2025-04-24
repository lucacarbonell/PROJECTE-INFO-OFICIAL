from graph import *


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


print("Probando el grafo...")
G = CreateGraph_1()
Plot(G)
PlotNode(G, "C")

n = GetClosest(G, 15, 5)
print(n.name)  # La respuesta debe ser J
n = GetClosest(G, 8, 19)
print(n.name)  # La respuesta debe ser B

# Probar el segundo grafo
G2 = CreateGraph_2()
Plot(G2)

# Probar carga desde archivo
print("\nProbando carga desde archivo...")
G_file = LoadGraphFromFile("graph_data.txt")
if G_file:
    Plot(G_file)
    SaveGraphToFile(G_file, "graph_data_saved.txt")