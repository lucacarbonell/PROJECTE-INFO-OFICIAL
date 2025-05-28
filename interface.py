import tkinter as tk
from tkinter import filedialog
from airSpace import airSpace
from path import a_star
from path import a_star, bfs_fallback
from matplotlib.patches import Arrow
from tkinter import messagebox
import traceback
import os
import time
import platform
import subprocess
import traceback

import matplotlib.pyplot as plt

# Crear instancia del espacio aéreo
airspace = airSpace()

# -------------------- CARGA DE ARCHIVOS --------------------

def load_files():
    filepaths = filedialog.askopenfilenames(
        title="Seleccione los 3 archivos (nav, seg, aer)",
        filetypes=[("Text files", "*.txt")]
    )

    if len(filepaths) != 3:
        messagebox.showerror("Error", "Debe seleccionar exactamente 3 archivos")
        return

    global airspace
    airspace = airSpace()
    airspace.load_from_files(*filepaths)

    # Mostrar resumen en consola
    print(f"\n✅ Datos cargados:")
    print(f"- Nodos: {len(airspace.navpoints)}")
    print(f"- Segmentos: {len(airspace.navsegments)}")
    print(f"- Aeropuertos: {len(airspace.navairports)}\n")

    status_label.config(
        text=f"✅ Datos cargados: {len(airspace.navpoints)} nodos, {len(airspace.navsegments)} segmentos")
    plot_complete_map()  # Mostrar el mapa automáticamente

# -------------------- REACHABILITY --------------------

def show_reachability():
    origin_name = entry_origin.get().strip().upper()
    origin = airspace.get_navpoint_by_name(origin_name)

    if not origin:
        output_text.insert(tk.END, f"❌ Nodo '{origin_name}' no encontrado\n")
        return

    # Obtener nodos alcanzables
    direct_reachable = airspace.get_direct_reachable(origin)

    # Mostrar en interfaz
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, f"Nodos directamente alcanzables desde {origin.name}:\n")

    for node in direct_reachable:
        seg = next((s for s in airspace.navsegments
                    if s.origin_number == origin.number and s.destination_number == node.number), None)
        distance = f"{seg.distance:.1f} km" if seg else "? km"
        output_text.insert(tk.END, f"- {node.name} ({distance})\n")

    # Mostrar en matplotlib
    plot_direct_reachability(airspace, origin, direct_reachable)

    # ===== NUEVA FUNCIONALIDAD: EXPORTAR A GOOGLE EARTH =====
    try:
        from kml_generator import create_reachability_kml, open_kml_in_google_earth

        # Crear nombre de archivo en directorio temporal
        import tempfile
        timestamp = int(time.time())
        kml_filename = os.path.join(tempfile.gettempdir(), f"reachable_{origin.name}_{timestamp}.kml")

        print(f"\n=== INICIANDO GENERACIÓN KML ===")
        print(f"Origen: {origin.name} ({origin.latitude}, {origin.longitude})")
        print(f"Nodos alcanzables: {len(direct_reachable)}")

        # Generar KML
        if create_reachability_kml(origin, direct_reachable, airspace, kml_filename):
            # Verificar archivo
            if os.path.exists(kml_filename):
                # Abrir en Google Earth
                if open_kml_in_google_earth(kml_filename):
                    output_text.insert(tk.END, "\n✅ Visualización abierta en Google Earth")
                else:
                    output_text.insert(tk.END, f"\n⚠️ Archivo generado: {kml_filename}")
            else:
                output_text.insert(tk.END, f"\n❌ Error: Archivo no creado")
        else:
            output_text.insert(tk.END, "\n❌ Error al generar KML")

    except Exception as e:
        output_text.insert(tk.END, f"\n❌ Error: {str(e)}")
        print(f"Error completo: {traceback.format_exc()}")

# -------------------- SHORTEST PATH --------------------
def plot_path_with_arrows(airspace, path):
    plt.figure(figsize=(12, 10))

    # 1. Dibujar TODOS los nodos (en gris)
    for np in airspace.navpoints.values():
        plt.plot(np.longitude, np.latitude, 'o', color='gray', markersize=6)
        plt.text(np.longitude, np.latitude + 0.05, np.name, fontsize=8, color='gray')

    # 2. Resaltar los nodos del camino (en rojo)
    for point in path.points:
        plt.plot(point.longitude, point.latitude, 'o', color='red', markersize=8)
        plt.text(point.longitude, point.latitude + 0.07, point.name,
                 fontsize=9, color='red', weight='bold')

    # 3. Dibujar SOLO los segmentos del camino (con flechas)
    for i in range(len(path.points) - 1):
        a = path.points[i]
        b = path.points[i + 1]

        # Buscar el segmento correspondiente
        segment = None
        for seg in airspace.navsegments:
            if (seg.origin_number == a.number and
                    seg.destination_number == b.number):
                segment = seg
                break

        if segment:
            dx = b.longitude - a.longitude
            dy = b.latitude - a.latitude

            # Dibujar línea base
            plt.plot([a.longitude, b.longitude],
                     [a.latitude, b.latitude],
                     color='red', linewidth=2, alpha=0.7)

            # Dibujar flecha
            plt.arrow(a.longitude, a.latitude,
                      dx * 0.85, dy * 0.85,  # Acortar flecha
                      head_width=0.03, head_length=0.04,
                      fc='red', ec='red',
                      length_includes_head=True)

            # Mostrar distancia del segmento
            mid_x = (a.longitude + b.longitude) / 2
            mid_y = (a.latitude + b.latitude) / 2
            plt.text(mid_x, mid_y, f"{segment.distance:.1f}km",
                     fontsize=8, bbox=dict(facecolor='white', alpha=0.8))

    plt.title(f"Camino más corto: {path.points[0].name} → {path.points[-1].name}", pad=20)
    plt.xlabel("Longitud")
    plt.ylabel("Latitud")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

def plot_complete_map():
    if not airspace.navpoints:
        return

    plt.figure(figsize=(14, 10))

    # Configuración del gráfico
    plt.title("Red Completa de Navegación Aérea", fontsize=14, pad=20)
    plt.xlabel("Longitud")
    plt.ylabel("Latitud")
    plt.grid(True, alpha=0.2)

    # 1. Dibujar TODOS los nodos (del mismo tamaño)
    for np in airspace.navpoints.values():
        plt.plot(np.longitude, np.latitude, 'o',
                 color='#1f77b4',  # Azul estándar
                 markersize=6,
                 alpha=0.9)
        plt.text(np.longitude, np.latitude + 0.04, np.name,
                 fontsize=7,
                 color='black',
                 ha='center')

    # 2. Dibujar TODOS los segmentos con flechas delgadas y precisas
    for seg in airspace.navsegments:
        origin = airspace.navpoints.get(seg.origin_number)
        dest = airspace.navpoints.get(seg.destination_number)

        if origin and dest:
            dx = dest.longitude - origin.longitude
            dy = dest.latitude - origin.latitude
            distance = (dx ** 2 + dy ** 2) ** 0.5

            # Ajuste para que la flecha toque el borde del nodo
            arrow_length = distance - 0.015  # 0.015 es el radio efectivo del nodo

            # Flecha más delgada (linewidth=1) y precisa
            plt.arrow(origin.longitude, origin.latitude,
                      dx * (arrow_length / distance), dy * (arrow_length / distance),
                      head_width=0.015,  # Más delgado
                      head_length=0.02,  # Más corto
                      fc='#2ca02c',  # Verde
                      ec='#2ca02c',
                      linewidth=1,  # Línea más fina
                      length_includes_head=True,
                      alpha=0.7)  # Ligera transparencia

            # Mostrar distancia (opcional)
            mid_x = origin.longitude + dx * 0.45
            mid_y = origin.latitude + dy * 0.45
            plt.text(mid_x, mid_y, f"{seg.distance:.1f}km",
                     fontsize=6,
                     bbox=dict(facecolor='white', alpha=0.7))

    plt.tight_layout()
    plt.show()


def show_shortest_path():
    origin_name = entry_origin.get().strip().upper()
    destination_name = entry_destination.get().strip().upper()
    output_text.delete(1.0, tk.END)

    # Función auxiliar para encontrar segmentos
    def find_segment(airspace, origin, destination):
        for seg in airspace.navsegments:
            if seg.origin_number == origin.number and seg.destination_number == destination.number:
                return seg
        return None

    # Buscar puntos (nodos normales o aeropuertos)
    origin = airspace.get_navpoint_by_name(origin_name)
    destination = airspace.get_navpoint_by_name(destination_name)

    # Búsqueda alternativa para aeropuertos
    if not origin:
        origin_airport = airspace.find_airport(origin_name)
        if origin_airport and origin_airport.sids:
            origin = origin_airport.sids[0]

    if not destination:
        dest_airport = airspace.find_airport(destination_name)
        if dest_airport and dest_airport.stars:
            destination = dest_airport.stars[0]

    # Validación
    if not origin or not destination:
        output_text.insert(tk.END, "❌ Nodos no encontrados. Verifique:\n")
        if not origin:
            output_text.insert(tk.END, f"- Origen '{origin_name}' no existe\n")
        if not destination:
            output_text.insert(tk.END, f"- Destino '{destination_name}' no existe\n")

        # Mostrar nodos disponibles
        available_nodes = sorted([np.name for np in airspace.navpoints.values()])
        output_text.insert(tk.END, "\nPrimeros 10 nodos disponibles:\n")
        for node in available_nodes[:10]:
            output_text.insert(tk.END, f"- {node}\n")
        return

    # Buscar camino con A*
    try:
        result = a_star(airspace, origin, destination)

        if not result:
            output_text.insert(tk.END, "❌ No existe conexión entre los nodos\n")
            return

        # Calcular distancia total y detalles
        total_distance = 0.0
        path_details = []
        for i in range(len(result.points) - 1):
            seg = find_segment(airspace, result.points[i], result.points[i + 1])
            if seg:
                total_distance += seg.distance
                path_details.append(f"{result.points[i].name} → {result.points[i + 1].name}: {seg.distance:.1f} km")

        # Mostrar resultados en texto
        output_text.insert(tk.END, f"✅ Camino encontrado ({len(result.points)} nodos):\n")
        output_text.insert(tk.END, " → ".join(p.name for p in result.points) + "\n\n")
        output_text.insert(tk.END, f"📏 Distancia total: {total_distance:.2f} km\n\n")
        output_text.insert(tk.END, "Detalle por segmentos:\n")
        for detail in path_details:
            output_text.insert(tk.END, f"- {detail}\n")

        # Configuración de visualización
        plt.close('all')  # Cerrar cualquier mapa previo
        fig, ax = plt.subplots(figsize=(14, 10))

        # Estilos visuales
        SEGMENT_COLOR = '#00CED1'  # Azul turquesa
        NODE_COLOR = 'black'
        ARROW_HEAD_WIDTH = 0.02
        ARROW_HEAD_LENGTH = 0.03

        # Dibujar todos los nodos (fondo)
        for np in airspace.navpoints.values():
            ax.plot(np.longitude, np.latitude, 'o',
                    color='lightgray',
                    markersize=4,
                    alpha=0.4)
            ax.text(np.longitude, np.latitude + 0.03, np.name,
                    fontsize=6,
                    color='gray',
                    ha='center')

        # Dibujar el camino encontrado
        for i in range(len(result.points) - 1):
            a = result.points[i]
            b = result.points[i + 1]
            dx = b.longitude - a.longitude
            dy = b.latitude - a.latitude
            dist = (dx ** 2 + dy ** 2) ** 0.5

            # Flecha turquesa grande
            ax.arrow(a.longitude, a.latitude,
                     dx * (dist - 0.015) / dist, dy * (dist - 0.015) / dist,
                     head_width=ARROW_HEAD_WIDTH,
                     head_length=ARROW_HEAD_LENGTH,
                     fc=SEGMENT_COLOR,
                     ec=SEGMENT_COLOR,
                     linewidth=1.8,
                     length_includes_head=True)

        # Resaltar nodos del camino
        for point in result.points:
            ax.plot(point.longitude, point.latitude, 'o',
                    color=NODE_COLOR,
                    markersize=7)
            ax.text(point.longitude, point.latitude + 0.04, point.name,
                    fontsize=9,
                    weight='bold',
                    color=NODE_COLOR,
                    ha='center')

        # Mostrar distancia total
        ax.text(0.5, 0.02, f"Distancia total: {total_distance:.2f} km",
                transform=ax.transAxes,
                fontsize=11,
                weight='bold',
                ha='center',
                bbox=dict(facecolor='white', edgecolor='black', alpha=0.9))

        plt.title("Camino más corto encontrado", pad=20)
        plt.xlabel("Longitud")
        plt.ylabel("Latitud")
        plt.grid(True, alpha=0.2)
        plt.tight_layout()
        plt.show()

        # ===== EXPORTAR Y ABRIR EN GOOGLE EARTH =====
        from path import export_path_to_kml, open_kml_in_google_earth

        # Generar nombre de archivo único con timestamp
        timestamp = int(time.time())
        kml_filename = f"shortest_path_{origin.name}_to_{destination.name}_{timestamp}.kml"

        # Depuración: mostrar puntos de la ruta
        print(f"Exportando ruta con {len(result.points)} puntos a {kml_filename}")
        for i, point in enumerate(result.points):
            print(f"Punto {i + 1}: {point.name} ({point.latitude}, {point.longitude})")

        # Exportar ruta completa con nodos
        if export_path_to_kml(result.points, kml_filename):
            print(f"Archivo KML generado: {os.path.abspath(kml_filename)}")

            # Verificar creación del archivo
            if os.path.exists(kml_filename):
                # Abrir inmediatamente en Google Earth
                if open_kml_in_google_earth(kml_filename):
                    output_text.insert(tk.END, "\n✅ Ruta abierta en Google Earth")
                else:
                    abs_path = os.path.abspath(kml_filename)
                    output_text.insert(tk.END, f"\n⚠️ No se pudo abrir automáticamente")
                    output_text.insert(tk.END, f"\nPor favor abre manualmente: {abs_path}")
            else:
                output_text.insert(tk.END, f"\n❌ Error: Archivo no creado - {kml_filename}")
        else:
            output_text.insert(tk.END, "\n❌ Error al exportar la ruta a KML")

    except Exception as e:
        output_text.insert(tk.END, f"❌ Error inesperado: {str(e)}\n")
        print(f"Error completo en show_shortest_path: {traceback.format_exc()}")


# -------------------- BUSCADOR DE AEROPUERTOS CERCANOS --------------------
def find_nearby_airports():
    try:
        # Obtener punto central
        center_name = entry_origin.get().strip().upper()
        center = airspace.get_navpoint_by_name(center_name)
        if not center:
            output_text.insert(tk.END, f"❌ Punto central '{center_name}' no encontrado\n")
            return

        # Obtener radio
        try:
            radius_km = float(entry_radius.get())
        except:
            output_text.insert(tk.END, "❌ Radio inválido. Use números (ej: 50.0)\n")
            return

        # Buscar aeropuertos en el radio
        nearby_airports = []
        for airport in airspace.navairports.values():
            if airport.sids:
                airport_point = airport.sids[0]
                # Calcular distancia en kilómetros (1 grado ≈ 111 km)
                distance = center.distance_to(airport_point) * 111
                if distance <= radius_km:
                    nearby_airports.append((airport, distance))

        # Mostrar resultados
        output_text.delete(1.0, tk.END)
        if not nearby_airports:
            output_text.insert(tk.END, f"❌ No hay aeropuertos dentro de {radius_km} km de {center.name}\n")
            return

        output_text.insert(tk.END, f"✈️ Aeropuertos dentro de {radius_km} km de {center.name}:\n")
        for airport, dist in sorted(nearby_airports, key=lambda x: x[1]):
            output_text.insert(tk.END, f"- {airport.name}: {dist:.1f} km\n")

        # Generar KML y abrir en Google Earth
        from kml_generator import generate_airports_radius_kml
        if generate_airports_radius_kml(center, nearby_airports, radius_km):
            output_text.insert(tk.END, "\n✅ Visualización abierta en Google Earth")

    except Exception as e:
        output_text.insert(tk.END, f"❌ Error: {str(e)}\n")
        print(f"Error en find_nearby_airports: {traceback.format_exc()}")


# -------------------- INTERFAZ GRÁFICA --------------------
# (Aquí comienza el código de creación de ventanas y widgets)
window = tk.Tk()
window.title("Explorador del Espacio Aéreo V4")


# -------------------- VISUALIZACIÓN --------------------

def plot_direct_reachability(airspace, origin, direct_reachable):
    plt.figure(figsize=(14, 10))

    # Configuración del gráfico
    plt.title(f"Conexiones DIRECTAS desde {origin.name}", fontsize=14, pad=20)
    plt.xlabel("Longitud")
    plt.ylabel("Latitud")
    plt.grid(True, alpha=0.3)

    # 1. Dibujar TODOS los nodos (mismo tamaño y con nombre)
    for np in airspace.navpoints.values():
        # Color diferente para nodos alcanzables vs otros
        color = 'black' if np in direct_reachable else 'red' if np == origin else 'grey'
        plt.plot(np.longitude, np.latitude, 'o',
                 color=color,
                 markersize=7,  # Mismo tamaño para todos
                 alpha=0.8)
        plt.text(np.longitude, np.latitude + 0.05, np.name,
                 fontsize=7,
                 ha='center',
                 color='black' if np in direct_reachable or np == origin else '#666666')

    # 2. Dibujar FLECHAS PRECISAS que tocan los nodos
    for neighbor in direct_reachable:
        dx = neighbor.longitude - origin.longitude
        dy = neighbor.latitude - origin.latitude
        distance = ((dx) ** 2 + (dy) ** 2) ** 0.5

        # Flecha que llega exactamente al borde del nodo
        arrow_length = distance - 0.02  # Ajuste para tocar el borde

        plt.arrow(origin.longitude, origin.latitude,
                  dx * (arrow_length / distance), dy * (arrow_length / distance),
                  head_width=0.02,
                  head_length=0.03,
                  fc='#00CED1',
                  ec='#00CED1',
                  linewidth=2,
                  length_includes_head=True)

        # Mostrar distancia
        mid_x = origin.longitude + dx * 0.45
        mid_y = origin.latitude + dy * 0.45
        seg = next((s for s in airspace.navsegments
                    if s.origin_number == origin.number and s.destination_number == neighbor.number), None)
        if seg:
            plt.text(mid_x, mid_y, f"{seg.distance:.1f} km",
                     fontsize=8,
                     bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))

    # Leyenda mejorada
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', label='Origen',
                   markerfacecolor='red', markersize=10),
        plt.Line2D([0], [0], marker='o', color='w', label='Alcanzable directo',
                   markerfacecolor='black', markersize=10),
        plt.Line2D([0], [0], marker='o', color='w', label='Otros nodos',
                   markerfacecolor='grey', markersize=10)
    ]
    plt.legend(handles=legend_elements, loc='upper right')

    plt.tight_layout()
    plt.show()

def plot_shortest_path(airspace, path):
    plt.figure(figsize=(10, 8))

    # Dibuja todos los nodos en gris
    for np in airspace.navpoints.values():
        plt.plot(np.longitude, np.latitude, 'o', color='gray', markersize=3)
        plt.text(np.longitude + 0.01, np.latitude + 0.01, np.name, fontsize=6)

    # Dibuja todos los segmentos en gris claro
    for seg in airspace.navsegments:
        p1 = airspace.navpoints.get(seg.origin_number)
        p2 = airspace.navpoints.get(seg.destination_number)
        if p1 and p2:
            plt.plot([p1.longitude, p2.longitude],
                     [p1.latitude, p2.latitude],
                     '-', color='lightgray', linewidth=0.5)

    # Resalta el camino encontrado en rojo
    for i in range(len(path.points) - 1):
        a = path.points[i]
        b = path.points[i + 1]
        plt.plot([a.longitude, b.longitude],
                 [a.latitude, b.latitude],
                 '-', color='red', linewidth=2)
        plt.plot(a.longitude, a.latitude, 'o', color='red', markersize=5)

    # Dibuja el último punto
    if path.points:
        last = path.points[-1]
        plt.plot(last.longitude, last.latitude, 'o', color='red', markersize=5)

    plt.title(f"Camino más corto: {' → '.join(p.name for p in path.points)}")
    plt.xlabel("Longitud")
    plt.ylabel("Latitud")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_airport_path(airspace, path, origin_name, dest_name):
    plt.close('all')
    fig, ax = plt.subplots(figsize=(14, 10))

    # Función auxiliar para encontrar segmentos
    def find_segment(airspace, origin, destination):
        for seg in airspace.navsegments:
            if seg.origin_number == origin.number and seg.destination_number == destination.number:
                return seg
        return None

    # 1. Configuración de estilos
    SEGMENT_COLOR = '#00CED1'  # Azul turquesa
    NODE_COLOR = 'black'
    ARROW_HEAD_WIDTH = 0.02  # 40% más grande que antes
    ARROW_HEAD_LENGTH = 0.03

    # 2. Dibujar TODOS los nodos (fondo atenuado)
    for np in airspace.navpoints.values():
        ax.plot(np.longitude, np.latitude, 'o',
                color='lightgray',
                markersize=4,
                alpha=0.4)
        ax.text(np.longitude, np.latitude + 0.03, np.name,
                fontsize=6,
                color='gray',
                ha='center',
                alpha=0.6)

    # 3. Calcular y dibujar el camino
    total_distance = 0.0
    for i in range(len(path.points) - 1):
        a = path.points[i]
        b = path.points[i + 1]
        seg = find_segment(airspace, a, b)
        if seg:
            total_distance += seg.distance

            # Dibujar segmento con flecha grande
            dx = b.longitude - a.longitude
            dy = b.latitude - a.latitude
            dist = (dx ** 2 + dy ** 2) ** 0.5
            adjust = dist - 0.015  # Ajuste para tocar el nodo

            ax.arrow(a.longitude, a.latitude,
                     dx * (adjust / dist), dy * (adjust / dist),
                     head_width=ARROW_HEAD_WIDTH,
                     head_length=ARROW_HEAD_LENGTH,
                     fc=SEGMENT_COLOR,
                     ec=SEGMENT_COLOR,
                     linewidth=1.8,
                     length_includes_head=True,
                     zorder=3)  # Para que aparezca sobre otros elementos

    # 4. Resaltar nodos del camino
    for point in path.points:
        ax.plot(point.longitude, point.latitude, 'o',
                color=NODE_COLOR,
                markersize=7,
                zorder=4)
        ax.text(point.longitude, point.latitude + 0.04, point.name,
                fontsize=9,
                weight='bold',
                color=NODE_COLOR,
                ha='center',
                zorder=5)

    # 5. Información de distancia
    distance_text = ax.text(0.5, 0.02, f"Distancia total: {total_distance:.2f} km",
                            transform=ax.transAxes,
                            fontsize=11,
                            weight='bold',
                            ha='center',
                            bbox=dict(facecolor='white', edgecolor=NODE_COLOR, alpha=0.9))

    # 6. Configuración final
    ax.set_title("Camino más corto encontrado", pad=20, fontsize=12, weight='bold')
    ax.set_xlabel("Longitud", fontsize=10)
    ax.set_ylabel("Latitud", fontsize=10)
    ax.grid(True, alpha=0.2)
    plt.tight_layout()
    plt.show()

# -------------------- PIRADA ----------------------
# -------------------- INTERFAZ --------------------

window = tk.Tk()
window.title("Explorador del Espacio Aéreo V4")

btn_load = tk.Button(window, text="Cargar archivos", command=load_files)
btn_load.pack(pady=5)

entry_origin = tk.Entry(window)
entry_origin.insert(0, "GODOX")
entry_origin.pack(pady=2)
entry_origin_label = tk.Label(window, text="Nodo origen")
entry_origin_label.pack()

entry_destination = tk.Entry(window)
entry_destination.insert(0, "SUKET")
entry_destination.pack(pady=2)
entry_destination_label = tk.Label(window, text="Nodo destino")
entry_destination_label.pack()

btn_reach = tk.Button(window, text="Mostrar alcanzables", command=show_reachability)
btn_reach.pack(pady=5)

btn_path = tk.Button(window, text="Camino más corto", command=show_shortest_path)
btn_path.pack(pady=5)

btn_export_kml = tk.Button(window, text="Exportar a KML", command=lambda: airspace.export_to_kml())
btn_export_kml.pack(pady=5)

entry_radius = tk.Entry(window, width=10)
entry_radius.pack(pady=2)
entry_radius_label = tk.Label(window, text="Radio de búsqueda (km)")
entry_radius_label.pack()

btn_find_airports = tk.Button(
    window,
    text="Buscar aeropuertos cercanos",
    command=find_nearby_airports,
    bg="#9C27B0",  # Color morado
    fg="white"
)
btn_find_airports.pack(pady=10)

output_text = tk.Text(window, height=15, width=60)
output_text.pack(pady=5)

status_label = tk.Label(window, text="Esperando carga de archivos...")
status_label.pack(pady=5)

window.mainloop()
