from node import node, Distance

class segment:
    def __init__(self, name: str, origin: node, destination: node):
        self.name = name
        self.origin = origin
        self.destination = destination
        self.cost = Distance(origin, destination)
