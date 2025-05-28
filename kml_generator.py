import subprocess
import platform
import os
import traceback
def create_kml_point(navpoint, name="", description=""):
    """Genera puntos amarillos para nodos regulares"""
    name = name if name else navpoint.name
    return f"""<Placemark>
    <name>{name}</name>
    <description>{description or f"NavPoint {navpoint.number}"}</description>
    <Style>
        <IconStyle>
            <color>ff00ffff</color>  <!-- Amarillo (formato aabbggrr) -->
            <scale>0.7</scale>
            <Icon>
                <href>http://maps.google.com/mapfiles/kml/shapes/shaded_dot.png</href>
            </Icon>
        </IconStyle>
    </Style>
    <Point>
        <coordinates>{navpoint.longitude},{navpoint.latitude},0</coordinates>
    </Point>
</Placemark>"""

def create_kml_line(path_points, name="Ruta", description=""):
    """Genera una línea KML para una lista de puntos (ruta)."""
    coordinates = " ".join(f"{p.longitude},{p.latitude},0" for p in path_points)
    return f"""<Placemark>
    <name>{name}</name>
    <description>{description}</description>
    <LineString>
        <coordinates>{coordinates}</coordinates>
    </LineString>
</Placemark>"""

def generate_kml_file(content, filename="output.kml"):
    """Guarda el contenido KML en un archivo con formato válido"""
    kml_template = f"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
    <name>{filename}</name>
    {content}
</Document>
</kml>"""

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(kml_template)
    print(f"Archivo {filename} generado correctamente")


def create_kml_airport(airport, navpoints):
    """Genera un marcador de aeropuerto con chincheta roja"""
    if not airport.sids:
        return ""

    first_point = airport.sids[0]
    return f"""<Placemark>
    <name>{airport.name} (Aeropuerto)</name>
    <Style>
        <IconStyle>
            <color>ff0000ff</color>  <!-- Rojo (formato aabbggrr) -->
            <scale>1.3</scale>
            <Icon>
                <href>http://maps.google.com/mapfiles/kml/pushpin/red-pushpin.png</href>
            </Icon>
        </IconStyle>
    </Style>
    <Point>
        <coordinates>{first_point.longitude},{first_point.latitude},0</coordinates>
    </Point>
    <description>Tipo: Aeropuerto\nSIDs: {len(airport.sids)}\nSTARs: {len(airport.stars)}</description>
</Placemark>"""

def open_kml_in_google_earth(kml_filepath):
    """Abre el archivo KML en Google Earth (multi-plataforma)"""
    try:
        if platform.system() == 'Windows':
            # Para Windows
            os.startfile(kml_filepath)
        elif platform.system() == 'Darwin':
            # Para macOS
            subprocess.run(['open', '-a', 'Google Earth', kml_filepath])
        else:
            # Para Linux (requiere google-earth-pro instalado)
            subprocess.run(['google-earth-pro', kml_filepath])
        return True
    except Exception as e:
        print(f"Error al abrir Google Earth: {e}")
        return False


def create_reachability_kml(origin, reachable_nodes, airspace, filename):
    """Genera KML para nodos alcanzables desde un origen - Versión robusta"""
    try:
        # Verificar datos de entrada
        if not origin or not reachable_nodes:
            print("Error: Datos insuficientes para generar KML")
            return False

        print(f"Generando KML para {len(reachable_nodes)} nodos alcanzables desde {origin.name}")

        # Crear contenido KML
        kml_content = []

        # Cabecera del documento
        kml_content.append('<?xml version="1.0" encoding="UTF-8"?>')
        kml_content.append('<kml xmlns="http://www.opengis.net/kml/2.2">')
        kml_content.append('<Document>')

        # Estilos
        kml_content.append("""
        <Style id="origin_style">
            <IconStyle>
                <color>ff00ff00</color>  <!-- Verde -->
                <scale>1.5</scale>
            </IconStyle>
        </Style>""")

        kml_content.append("""
        <Style id="node_style">
            <IconStyle>
                <color>ff00ffff</color>  <!-- Amarillo -->
                <scale>0.7</scale>
                <Icon>
                    <href>http://maps.google.com/mapfiles/kml/shapes/shaded_dot.png</href>
                </Icon>
            </IconStyle>
        </Style>""")

        kml_content.append("""
        <Style id="segment_style">
            <LineStyle>
                <color>ff0000ff</color>  <!-- Rojo -->
                <width>2</width>
            </LineStyle>
        </Style>""")

        # Nodo origen
        kml_content.append(f"""
        <Placemark>
            <name>ORIGEN: {origin.name}</name>
            <styleUrl>#origin_style</styleUrl>
            <Point>
                <coordinates>{origin.longitude},{origin.latitude},0</coordinates>
            </Point>
        </Placemark>""")

        # Nodos alcanzables y segmentos
        for node in reachable_nodes:
            # Nodo alcanzable
            kml_content.append(f"""
            <Placemark>
                <name>{node.name}</name>
                <styleUrl>#node_style</styleUrl>
                <Point>
                    <coordinates>{node.longitude},{node.latitude},0</coordinates>
                </Point>
            </Placemark>""")

            # Buscar segmento
            seg = None
            for s in airspace.navsegments:
                if s.origin_number == origin.number and s.destination_number == node.number:
                    seg = s
                    break

            # Añadir segmento si existe
            if seg:
                kml_content.append(f"""
                <Placemark>
                    <name>{origin.name} → {node.name}</name>
                    <description>Distancia: {seg.distance:.1f} km</description>
                    <styleUrl>#segment_style</styleUrl>
                    <LineString>
                        <coordinates>
                            {origin.longitude},{origin.latitude},0
                            {node.longitude},{node.latitude},0
                        </coordinates>
                    </LineString>
                </Placemark>""")

        # Cerrar documento
        kml_content.append('</Document>')
        kml_content.append('</kml>')

        # Escribir archivo
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("\n".join(kml_content))

        print(f"KML generado exitosamente: {os.path.abspath(filename)}")
        print(f"Tamaño del archivo: {os.path.getsize(filename)} bytes")
        return True

    except Exception as e:
        print(f"Error en create_reachability_kml: {traceback.format_exc()}")
        return False


def generate_airports_radius_kml(center, airports_with_distances, radius_km):
    """Genera KML con aeropuertos en un radio y círculo de búsqueda"""
    try:
        content = []

        # 1. Círculo de radio
        circle_coords = []
        for angle in range(0, 360, 10):
            rad = angle * 3.1416 / 180
            dx = radius_km / 111 * math.cos(rad)
            dy = radius_km / 111 * math.sin(rad)
            circle_coords.append(f"{center.longitude + dx},{center.latitude + dy},0")

        content.append(f"""<Placemark>
            <name>Radio de {radius_km} km</name>
            <Style><LineStyle><color>7f00ffff</color><width>2</width></LineStyle></Style>
            <Polygon>
                <outerBoundaryIs>
                    <LinearRing>
                        <coordinates>{" ".join(circle_coords)}</coordinates>
                    </LinearRing>
                </outerBoundaryIs>
            </Polygon>
        </Placemark>""")

        # 2. Punto central
        content.append(f"""<Placemark>
            <name>Centro: {center.name}</name>
            <Style><IconStyle><color>ff0000ff</color><scale>1.5</scale></IconStyle></Style>
            <Point>
                <coordinates>{center.longitude},{center.latitude},0</coordinates>
            </Point>
        </Placemark>""")

        # 3. Aeropuertos encontrados
        for airport, distance in airports_with_distances:
            ap_point = airport.sids[0]
            content.append(f"""<Placemark>
                <name>{airport.name} ({distance:.1f} km)</name>
                <description>Aeropuerto</description>
                <Style><IconStyle><color>ff00ff00</color><scale>1.3</scale></IconStyle></Style>
                <Point>
                    <coordinates>{ap_point.longitude},{ap_point.latitude},0</coordinates>
                </Point>
            </Placemark>""")

        # Guardar archivo
        filename = f"airports_{center.name}_{radius_km}km.kml"
        generate_kml_file("\n".join(content), filename)

        # Abrir en Google Earth
        open_kml_in_google_earth(filename)

        return True
    except Exception as e:
        print(f"Error en generate_airports_radius_kml: {traceback.format_exc()}")
        return False