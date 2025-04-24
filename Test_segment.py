from node import Node
from segment import Segment

# Crear 3 nodos
n1 = Node('A', 1, 1)
n2 = Node('B', 4, 5)
n3 = Node('C', 8, 2)

# Crear segmentos
seg1 = Segment('AB', n1, n2)
seg2 = Segment('BC', n2, n3)

# Mostrar información
print("Segmento 1:")
print(f"Nombre: {seg1.name}")
print(f"Origen: {seg1.origin.name}")
print(f"Destino: {seg1.destination.name}")
print(f"Costo: {seg1.cost:.2f}")

print("\nSegmento 2:")
print(f"Nombre: {seg2.name}")
print(f"Origen: {seg2.origin.name}")
print(f"Destino: {seg2.destination.name}")
print(f"Costo: {seg2.cost:.2f}")
