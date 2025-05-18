class navPoint:
    def __init__(self, number, name, latitude, longitude):
        self.number = number
        self.name = name
        self.latitude = latitude
        self.longitude = longitude

    def _repr_(self):
        return f"NavPoint({self.number}, '{self.name}', {self.latitude}, {self.longitude})"

    def distance_to(self, other):
        dx = self.longitude - other.longitude
        dy = self.latitude - other.latitude
        return (dx**2 + dy**2)**0.5