from node import *

n1 = Node('aaa', 0, 0)
n2 = Node('bbb', 3, 4)
print(Distance(n1, n2))  # Debería mostrar 5.0
print(AddNeighbor(n1, n2))  # Debería mostrar True
print(AddNeighbor(n1, n2))  # Debería mostrar False
print(n1.__dict__)  # Mostrará los atributos de n1
for n in n1.neighbors:
    print(n.__dict__)  # Mostrará los atributos de los vecinos