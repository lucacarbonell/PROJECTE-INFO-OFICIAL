from navPoint import navPoint
from navSegment import navSegment
from navAirport import navAirport

class airSpace:
    def __init__(self):
        self.navpoints = {}
        self.navsegments = []
        self.navairports = {}

    def load_from_files(self, *filepaths):
        """Carga los 3 archivos en cualquier orden"""
        # Primero identificar qué archivo es cuál
        nav_file = None
        seg_file = None
        aer_file = None

        for filepath in filepaths:
            with open(filepath, 'r') as f:
                first_line = f.readline().strip()

                # Identificar por el contenido
                if len(first_line.split()) == 4:  # Formato de navpoints (ej: "1 GODOX 41.5 2.2")
                    nav_file = filepath
                elif len(first_line.split()) == 3:  # Formato de segments (ej: "1 2 50.0")
                    seg_file = filepath
                elif first_line.endswith('.D') or first_line.endswith('.A'):  # Aeropuertos (ej: "LEBL.D")
                    aer_file = filepath
                else:  # Por nombre de archivo como último recurso
                    if 'nav' in filepath.lower():
                        nav_file = filepath
                    elif 'seg' in filepath.lower():
                        seg_file = filepath
                    elif 'aer' in filepath.lower():
                        aer_file = filepath

        # Cargar los archivos identificados
        if nav_file:
            self._load_navpoints(nav_file)
        if seg_file:
            self._load_navsegments(seg_file)
        if aer_file:
            self._load_airports(aer_file)

    def _load_navpoints(self, filepath):
        with open(filepath, 'r') as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) >= 4:  # Formato: número nombre latitud longitud
                    number = int(parts[0])
                    name = parts[1]
                    latitude = float(parts[2])
                    longitude = float(parts[3])
                    self.navpoints[number] = navPoint(number, name, latitude, longitude)
                    print(f"Cargado: {name} ({number})")  # Debug

    def _load_navsegments(self, filepath):
        with open(filepath, 'r') as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) < 3:
                    continue
                origin = int(parts[0])
                destination = int(parts[1])
                distance = float(parts[2])
                print(f"Cargando segmendo: {origin} -> {destination} ({distance})")
                self.navsegments.append(navSegment(origin, destination, distance))

    def _load_airports(self, filepath):
        current_airport = None
        with open(filepath, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                if not line.endswith('.D') and not line.endswith('.A'):
                    # Es un nuevo aeropuerto
                    current_airport = navAirport(line)
                    self.navairports[line] = current_airport
                elif current_airport:
                    # Es un SID o STAR
                    name = line
                    navpoint = self.get_navpoint_by_name(name)
                    if navpoint:
                        if name.endswith('.D'):
                            current_airport.add_sid(navpoint)
                        elif name.endswith('.A'):
                            current_airport.add_star(navpoint)

    def get_navpoint_by_name(self, name):
        """Busca nodos ignorando mayúsculas/minúsculas y espacios"""
        name_clean = name.strip().upper()
        for np in self.navpoints.values():
            if np.name.upper() == name_clean:
                return np
        return None

    def get_neighbors(self, navpoint):
        # Devuelve lista de navPoints vecinos
        return [self.navpoints[seg.destination_number]
                for seg in self.navsegments
                if seg.origin_number == navpoint.number]

    def get_direct_reachable(self, origin):
        """Devuelve solo nodos alcanzables DIRECTAMENTE (1 salto)"""
        direct_neighbors = []
        for seg in self.navsegments:
            if seg.origin_number == origin.number:
                neighbor = self.navpoints.get(seg.destination_number)
                if neighbor:
                    direct_neighbors.append(neighbor)
        return direct_neighbors

    def find_airport(self, name):
        """Busca aeropuertos ignorando mayúsculas/minúsculas y espacios"""
        name_clean = name.strip().upper()
        for airport_name, airport in self.navairports.items():
            if airport_name.upper() == name_clean:
                return airport

            # Búsqueda flexible para códigos IATA/ICAO
            if len(name_clean) == 3:  # Si es un código IATA (ej: "BCN")
                if airport_name.startswith(name_clean):
                    return airport

        return None  # Si no se encuentra

    def _repr_(self):
        return (f"AirSpace: {len(self.navpoints)} navpoints, "
                f"{len(self.navsegments)} segments, "
                f"{len(self.navairports)} airports")

    def export_to_kml(self, filename="airspace.kml"):
        """Exporta todos los elementos a KML y lo abre en Google Earth"""
        from kml_generator import (
            create_kml_point,
            create_kml_line,
            create_kml_airport,
            generate_kml_file,
            open_kml_in_google_earth
        )

        # Verificar datos cargados
        if not self.navpoints:
            print("Error: No hay datos de navegación cargados")
            return False

        content = []

        # 1. Aeropuertos (chinchetas rojas)
        for airport in self.navairports.values():
            airport_kml = create_kml_airport(airport, self.navpoints)
            if airport_kml:
                content.append(airport_kml)

        # 2. Puntos de navegación (puntos amarillos)
        for np in self.navpoints.values():
            content.append(create_kml_point(np))

        # 3. Segmentos (líneas verdes)
        line_style = """<Style id="segment_style">
            <LineStyle><color>ff00ff00</color><width>2</width></LineStyle>
        </Style>"""
        content.append(line_style)

        for seg in self.navsegments:
            origin = self.navpoints.get(seg.origin_number)
            dest = self.navpoints.get(seg.destination_number)
            if origin and dest:
                content.append(create_kml_line(
                    [origin, dest],
                    name=f"{origin.name} → {dest.name}",
                    description=f"Distancia: {seg.distance:.1f} km"
                ))

        # Generar archivo
        generate_kml_file("\n".join(content), filename)

        # Abrir en Google Earth
        return open_kml_in_google_earth(filename)
