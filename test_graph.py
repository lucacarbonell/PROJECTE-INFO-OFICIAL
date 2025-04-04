from graph import *

def CreateGraph_1 ():
    G = Graph()
    AddNode(G, node("A",1,20))
    AddNode(G, node("B",8,17))
    AddNode(G, node("C",15,20))
    AddNode(G, node("D",18,15))
    AddNode(G, node("E",2,4))
    AddNode(G, node("F",6,5))
    AddNode(G, node("G",12,12))
    AddNode(G, node("H",10,3))
    AddNode(G, node("I",19,1))
    AddNode(G, node("J",13,5))
    AddNode(G, node("K",3,15))
    AddNode(G, node("L",4,10))
    AddSegment(G, "AB","A","B")
    AddSegment(G, "AE","A","E")
    AddSegment(G, "AK","A","K")
    AddSegment(G, "BA","B","A")
    AddSegment(G, "BC","B","C")
    AddSegment(G, "BF","B","F")
    AddSegment(G, "BK","B","K")
    AddSegment(G, "BG","B","G")
    AddSegment(G, "CD","C","D")
    AddSegment(G, "CG","C","G")
    AddSegment(G, "DG","D","G")
    AddSegment(G, "DH","D","H")
    AddSegment(G, "DI","D","I")
    AddSegment(G, "EF","E","F")
    AddSegment(G, "FL","F","L")
    AddSegment(G, "GB","G","B")
    AddSegment(G, "GF","G","F")
    AddSegment(G, "GH","G","H")
    AddSegment(G, "ID","I","D")
    AddSegment(G, "IJ","I","J")
    AddSegment(G, "JI","J","I")
    AddSegment(G, "KA","K","A")
    AddSegment(G, "KL","K","L")
    AddSegment(G, "LK","L","K")
    AddSegment(G, "LF","L","F")
    return G

def CreateGraph_2():
    H = Graph()

    # Afegim nodes inventats
    AddNode(H, node("A", 4, 8))
    AddNode(H, node("B", 2, 5))
    AddNode(H, node("C", 4, 1))
    AddNode(H, node("D", 7, 3))
    AddNode(H, node("E", 2, 2))
    AddNode(H, node("F", 1, 5))

    # Afegim segments inventats
    AddSegment(H, "AC", "A", "C")
    AddSegment(H, "DA", "D", "A")
    AddSegment(H, "CF", "C", "F")
    AddSegment(H, "FB", "F", "B")
    AddSegment(H, "EF", "E", "F")
    AddSegment(H, "AB", "A", "B")

    # Mostrar el gràfic creat
    return H

if __name__ == "__main__":
    print("Probando el grafo...")
    G = CreateGraph_1()
    Plot(G)
    PlotNode(G, "C")

    n = GetClosest(G, 15, 5)
    print(n.name)  # La respuesta debe ser J
    n = GetClosest(G, 8, 19)
    print(n.name)  # La respuesta debe ser B

    H = CreateGraph_2()
    Plot(H)


def CreateGraphFromFile():
    # Creem el graf des d'un fitxer
    H = CreateGraphFromFile("graph_data.txt")

    # Comprovem que els nodes es van afegir correctament
    assert len(H.nodes) > 0, "No s'han afegit nodes"

    # Comprovem que els segments es van afegir correctament
    assert len(H.segments) > 0, "No s'han afegit segments"

    # Verifiquem alguns valors específics
    node_names = [n.name for n in H.nodes]
    assert "A" in node_names, "Node A no trobat"
    assert "B" in node_names, "Node B no trobat"

    segment_names = [s.name for s in H.segments]
    assert "AB" in segment_names, "Segment AB no trobat"
    assert "AE" in segment_names, "Segment AE no trobat"

    # Mostrar el gràfic
    Plot(H)  # Aquesta línia permet visualitzar el gràfic creat



from graph import *


def CreateGraphFromFileTest(file_path):
    # Crear el gràfic des de fitxer
    G = Graph().CreateGraphFromFile(file_path)

    # Mostrar el gràfic creat
    Plot(G)

    # Comprovem que els nodes i segments han estat creats correctament
    print(f"Nodes creats: {[n.name for n in G.nodes]}")
    print(f"Segments creats: {[s.name for s in G.segments]}")


# Cridar la prova
if __name__ == "__main__":
    print("Provant la funció CreateGraphFromFile...")
    CreateGraphFromFileTest("graph_data.txt")  # Aquesta ruta ha de ser correcta

