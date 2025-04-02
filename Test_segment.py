from node import node
from segment import segment

n1 = node("A", 1, 3)
n2 = node("B", 3, 4)
n3 = node("C", 6, 9)

s1 = segment("Segment 1", n1, n2)
s2 = segment("Segment 2", n2, n3)

print(f"{s1.name}: {s1.origin.name} -> {s1.destination.name}, Cost: {s1.cost}")
print(f"{s2.name}: {s2.origin.name} -> {s2.destination.name}, Cost: {s2.cost}")
