class navSegment:
    def __init__(self, origin_number, destination_number, distance):
        self.origin_number = origin_number
        self.destination_number = destination_number
        self.distance = distance

    def _repr_(self):
        return (f"NavSegment(origin={self.origin_number}, "
                f"destination={self.destination_number}, distance={self.distance})")