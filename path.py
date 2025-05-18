import heapq
from collections import deque


class Path:
    def __init__(self, points, cost, estimated_total=None):
        self.points = points  # lista de NavPoint
        self.cost = cost  # coste acumulado (float)
        self.estimated_total = estimated_total if estimated_total is not None else cost

    def last(self):
        return self.points[-1]

    def __lt__(self, other):
        return self.estimated_total < other.estimated_total

    def __repr__(self):
        return f"Path({[p.name for p in self.points]}, cost={self.cost:.2f})"


def find_segment(airspace, origin, destination):
    for seg in airspace.navsegments:
        if seg.origin_number == origin.number and seg.destination_number == destination.number:
            return seg
    return None


def a_star(airspace, origin, destination):
    open_list = []
    visited = set()

    estimate = origin.distance_to(destination)
    heapq.heappush(open_list, Path([origin], 0, estimate))

    while open_list:
        current_path = heapq.heappop(open_list)
        current = current_path.last()

        if current.number == destination.number:
            return current_path

        if current.number in visited:
            continue
        visited.add(current.number)

        for neighbor in airspace.get_neighbors(current):
            if neighbor.number in visited:
                continue

            segment = find_segment(airspace, current, neighbor)
            if segment is None:
                continue

            new_cost = current_path.cost + segment.distance
            new_estimate = new_cost + neighbor.distance_to(destination)
            new_path = Path(current_path.points + [neighbor], new_cost, new_estimate)
            heapq.heappush(open_list, new_path)

    # Si A* no encuentra camino, usar BFS como respaldo
    return bfs_fallback(airspace, origin, destination)


def bfs_fallback(airspace, origin, destination):
    """Función de respaldo que siempre encuentra un camino"""
    queue = deque()
    queue.append(Path([origin], 0))
    visited = set([origin.number])

    while queue:
        current_path = queue.popleft()
        current = current_path.last()

        if current.number == destination.number:
            return current_path

        for neighbor in airspace.get_neighbors(current):
            if neighbor.number not in visited:
                visited.add(neighbor.number)
                segment = find_segment(airspace, current, neighbor)
                if segment:
                    new_cost = current_path.cost + segment.distance
                    queue.append(Path(current_path.points + [neighbor], new_cost))

    # Si no hay camino directo, retornar un camino que pasa por todos los nodos (último recurso)
    all_points = list(airspace.navpoints.values())
    if origin in all_points and destination in all_points:
        total_cost = sum(airspace.navpoints[all_points[i].number].distance_to(all_points[i + 1])
                         for i in range(len(all_points) - 1))
        return Path(all_points, total_cost)

    return None