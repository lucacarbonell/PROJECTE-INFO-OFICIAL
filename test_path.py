from path import *
from node import Node

# Crear nodos de prueba
n1 = Node("A", 0, 0)
n2 = Node("B", 3, 4)
n3 = Node("C", 6, 0)

# Probar la clase Path
print("=== Testing Path class ===")
path = Path([n1, n2], 5.0)
print(path)  # Debería mostrar: Path(nodes=['A', 'B'], cost=5.0)

# Probar AddNodeToPath
print("\n=== Testing AddNodeToPath ===")
new_path = AddNodeToPath(path, n3, 6.0)
print(new_path)  # Debería mostrar: Path(nodes=['A', 'B', 'C'], cost=11.0)

# Probar ContainsNode
print("\n=== Testing ContainsNode ===")
print(ContainsNode(path, n1))  # True
print(ContainsNode(path, n3))  # False

# Probar CostToNode
print("\n=== Testing CostToNode ===")
print(CostToNode(path, n1))  # 5.0 (simplificado)
print(CostToNode(path, n3))  # -1