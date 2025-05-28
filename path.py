import heapq
from collections import deque
import os
import subprocess
import platform
import traceback

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


def export_path_to_kml(path_points, filename="shortest_path.kml"):
    """Exporta la ruta completa con todos los nodos intermedios"""
    try:
        if not path_points:
            return False

        content = []

        # Estilo para la ruta (línea roja gruesa)
        content.append("""<Style id="route_style">
            <LineStyle><color>ff0000ff</color><width>4</width></LineStyle>
        </Style>""")

        # Estilo para los nodos (puntos amarillos)
        content.append("""<Style id="node_style">
            <IconStyle>
                <color>ff00ffff</color>
                <scale>0.7</scale>
                <Icon><href>http://maps.google.com/mapfiles/kml/shapes/shaded_dot.png</href></Icon>
            </IconStyle>
        </Style>""")

        # Estilo para origen (verde) y destino (rojo)
        content.append("""<Style id="origin_style">
            <IconStyle><color>ff00ff00</color><scale>1.5</scale></IconStyle>
        </Style>""")
        content.append("""<Style id="dest_style">
            <IconStyle><color>ffff0000</color><scale>1.5</scale></IconStyle>
        </Style>""")

        # Línea de la ruta
        coordinates = " ".join(f"{p.longitude},{p.latitude},0" for p in path_points)
        content.append(f"""<Placemark>
            <name>Ruta más corta</name>
            <description>Desde {path_points[0].name} a {path_points[-1].name}</description>
            <styleUrl>#route_style</styleUrl>
            <LineString>
                <coordinates>{coordinates}</coordinates>
            </LineString>
        </Placemark>""")

        # Marcadores para todos los nodos de la ruta
        for i, point in enumerate(path_points):
            style_id = "node_style"
            name = point.name

            if i == 0:
                style_id = "origin_style"
                name = f"ORIGEN: {name}"
            elif i == len(path_points) - 1:
                style_id = "dest_style"
                name = f"DESTINO: {name}"

            content.append(f"""<Placemark>
                <name>{name}</name>
                <styleUrl>#{style_id}</styleUrl>
                <Point>
                    <coordinates>{point.longitude},{point.latitude},0</coordinates>
                </Point>
            </Placemark>""")

        # Generar archivo KML
        kml_template = f"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
{"".join(content)}
</Document>
</kml>"""

        with open(filename, 'w') as f:
            f.write(kml_template)

        return True

    except Exception as e:
        print(f"Error en export_path_to_kml: {traceback.format_exc()}")
        return False


def open_kml_in_google_earth(kml_filepath):
    """Versión mejorada para abrir KML en cualquier sistema"""
    try:
        # Verificar que el archivo existe
        if not os.path.exists(kml_filepath):
            print(f"Error: Archivo no encontrado - {kml_filepath}")
            return False

        abs_path = os.path.abspath(kml_filepath)
        system = platform.system()

        print(f"Intentando abrir: {abs_path} en {system}")

        # Windows
        if system == 'Windows':
            try:
                os.startfile(abs_path)
                print("Abierto usando os.startfile()")
                return True
            except Exception as e:
                print(f"Error con os.startfile: {e}")
                # Intentar con comando
                try:
                    subprocess.run(f'start "" "{abs_path}"', shell=True)
                    return True
                except Exception as e2:
                    print(f"Error con subprocess: {e2}")

        # macOS
        elif system == 'Darwin':
            try:
                # Primero intentar con Google Earth Pro
                subprocess.run(['open', '-a', 'Google Earth Pro', abs_path])
                print("Abierto con Google Earth Pro")
                return True
            except:
                try:
                    # Luego con Google Earth normal
                    subprocess.run(['open', '-a', 'Google Earth', abs_path])
                    print("Abierto con Google Earth")
                    return True
                except:
                    # Último recurso
                    subprocess.run(['open', abs_path])
                    return True

        # Linux
        elif system == 'Linux':
            try:
                subprocess.run(['google-earth-pro', abs_path])
                return True
            except:
                try:
                    subprocess.run(['google-earth', abs_path])
                    return True
                except:
                    subprocess.run(['xdg-open', abs_path])
                    return True

        # Otros sistemas o fallos
        import webbrowser
        webbrowser.open(abs_path)
        return True

    except Exception as e:
        print(f"Error completo al abrir Google Earth: {traceback.format_exc()}")
        return False