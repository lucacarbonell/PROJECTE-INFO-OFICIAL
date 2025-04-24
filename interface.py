import tkinter as tk
from tkinter import filedialog, messagebox
from graph import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from node import Distance


class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Explorer - Version 1")
        self.current_graph = None

        # Frame principal
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Frame para controles
        self.control_frame = tk.Frame(self.main_frame)
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        # Frame para el gráfico
        self.graph_frame = tk.Frame(self.main_frame)
        self.graph_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Botones
        tk.Button(self.control_frame, text="Show Example Graph 1",
                  command=self.show_example_graph1).pack(fill=tk.X, pady=2)
        tk.Button(self.control_frame, text="Show Example Graph 2",
                  command=self.show_example_graph2).pack(fill=tk.X, pady=2)
        tk.Button(self.control_frame, text="Load Graph from File",
                  command=self.load_graph_from_file).pack(fill=tk.X, pady=2)
        tk.Button(self.control_frame, text="Show Node Neighbors",
                  command=self.show_node_neighbors).pack(fill=tk.X, pady=2)
        tk.Button(self.control_frame, text="Add Node",
                  command=self.add_node_dialog).pack(fill=tk.X, pady=2)
        tk.Button(self.control_frame, text="Add Segment",
                  command=self.add_segment_dialog).pack(fill=tk.X, pady=2)
        tk.Button(self.control_frame, text="Delete Node",
                  command=self.delete_node_dialog).pack(fill=tk.X, pady=2)
        tk.Button(self.control_frame, text="Create New Graph",
                  command=self.create_new_graph).pack(fill=tk.X, pady=2)
        tk.Button(self.control_frame, text="Save Graph to File",
                  command=self.save_graph_to_file).pack(fill=tk.X, pady=2)
        tk.Button(self.control_frame, text="Find Shortest Path",
                  command=self.show_shortest_path).pack(fill=tk.X, pady=2)



        # Área para mostrar el gráfico
        self.figure, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Estado inicial
        self.clear_graph_display()

    def clear_graph_display(self):
        self.ax.clear()
        self.ax.set_title("No graph loaded")
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.canvas.draw()

    def show_example_graph1(self):
        self.current_graph = CreateGraph_1()
        self.plot_current_graph()

    def show_example_graph2(self):
        self.current_graph = CreateGraph_2()
        self.plot_current_graph()

    def load_graph_from_file(self):
        filename = filedialog.askopenfilename(title="Select Graph File",
                                              filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        if filename:
            self.current_graph = LoadGraphFromFile(filename)
            if self.current_graph:
                self.plot_current_graph()
            else:
                messagebox.showerror("Error", "Failed to load graph from file")

    def show_node_neighbors(self):
        if not self.current_graph:
            messagebox.showwarning("Warning", "No graph loaded")
            return

        node_name = tk.simpledialog.askstring("Node Neighbors", "Enter node name:")
        if node_name:
            if not PlotNode(self.current_graph, node_name):
                messagebox.showerror("Error", f"Node '{node_name}' not found in graph")

    def show_shortest_path(self):
        if not self.current_graph or len(self.current_graph.nodes) < 2:
            messagebox.showwarning("Warning", "Not enough nodes in graph")
            return

        origin = tk.simpledialog.askstring("Shortest Path", "Enter origin node name:")
        if not origin:
            return

        destination = tk.simpledialog.askstring("Shortest Path", "Enter destination node name:")
        if not destination:
            return

        path = FindShortestPath(self.current_graph, origin, destination)
        if path:
            messagebox.showinfo("Shortest Path",
                                f"Path found with cost {path.cost:.1f}:\n{' -> '.join([node.name for node in path.nodes])}")
            self.plot_path(path)
        else:
            messagebox.showinfo("Shortest Path", "No path exists between these nodes")

    def plot_path(self, path):
        self.ax.clear()

        # Dibujar todos los segmentos en gris primero
        for seg in self.current_graph.segments:
            self.ax.plot([seg.origin.x, seg.destination.x],
                         [seg.origin.y, seg.destination.y],
                         'gray', linewidth=1, alpha=0.3)

        # Resaltar segmentos del camino más corto
        for i in range(len(path.nodes) - 1):
            origin = path.nodes[i]
            destination = path.nodes[i + 1]
            self.ax.plot([origin.x, destination.x],
                         [origin.y, destination.y],
                         'r-', linewidth=2)
            # Mostrar costo en rojo
            mid_x = (origin.x + destination.x) / 2
            mid_y = (origin.y + destination.y) / 2
            self.ax.text(mid_x, mid_y, f"{Distance(origin, destination):.1f}",
                         fontsize=8, ha='center', va='center', color='red',
                         bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))

        # Dibujar nodos
        for node in self.current_graph.nodes:
            if node in path.nodes:
                color = 'blue' if node == path.nodes[0] or node == path.nodes[-1] else 'green'
            else:
                color = 'gray'

            self.ax.plot(node.x, node.y, 'o', markersize=10, color=color)
            self.ax.text(node.x, node.y, node.name,
                         fontsize=12, ha='center', va='center', color='white')

        self.ax.grid(True)
        self.ax.set_title(f"Shortest Path from {path.nodes[0].name} to {path.nodes[-1].name}")
        self.canvas.draw()
    def plot_current_graph(self):
        if not self.current_graph:
            return

        self.ax.clear()

        # Dibujar segmentos
        for seg in self.current_graph.segments:
            self.ax.plot([seg.origin.x, seg.destination.x],
                         [seg.origin.y, seg.destination.y],
                         'k-', linewidth=1)
            # Mostrar costo en el medio del segmento
            mid_x = (seg.origin.x + seg.destination.x) / 2
            mid_y = (seg.origin.y + seg.destination.y) / 2
            self.ax.text(mid_x, mid_y, f"{seg.cost:.1f}",
                         fontsize=8, ha='center', va='center',
                         bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))

        # Dibujar nodos
        for node in self.current_graph.nodes:
            self.ax.plot(node.x, node.y, 'ko', markersize=10)
            self.ax.text(node.x, node.y, node.name,
                         fontsize=12, ha='center', va='center', color='white')

        self.ax.grid(True)
        self.ax.set_title("Graph Visualization")
        self.canvas.draw()

    def add_node_dialog(self):
        if not self.current_graph:
            messagebox.showwarning("Warning", "No graph loaded. Creating new graph.")
            self.current_graph = Graph()

        name = tk.simpledialog.askstring("Add Node", "Enter node name:")
        if name:
            # Verificar si el nodo ya existe
            for node in self.current_graph.nodes:
                if node.name == name:
                    messagebox.showerror("Error", f"Node '{name}' already exists")
                    return

            x = tk.simpledialog.askfloat("Add Node", "Enter X coordinate:")
            y = tk.simpledialog.askfloat("Add Node", "Enter Y coordinate:")

            if x is not None and y is not None:
                AddNode(self.current_graph, Node(name, x, y))
                self.plot_current_graph()

    def add_segment_dialog(self):
        if not self.current_graph or len(self.current_graph.nodes) < 2:
            messagebox.showwarning("Warning", "Not enough nodes in graph")
            return

        origin = tk.simpledialog.askstring("Add Segment", "Enter origin node name:")
        if not origin:
            return

        destination = tk.simpledialog.askstring("Add Segment", "Enter destination node name:")
        if not destination:
            return

        # Verificar que los nodos existen
        origin_exists = any(node.name == origin for node in self.current_graph.nodes)
        destination_exists = any(node.name == destination for node in self.current_graph.nodes)

        if not origin_exists or not destination_exists:
            messagebox.showerror("Error", "One or both nodes not found in graph")
            return

        segment_name = f"{origin}{destination}"
        if AddSegment(self.current_graph, segment_name, origin, destination):
            self.plot_current_graph()
        else:
            messagebox.showerror("Error", "Failed to add segment")

    def delete_node_dialog(self):
        if not self.current_graph or not self.current_graph.nodes:
            messagebox.showwarning("Warning", "No nodes in graph")
            return

        node_name = tk.simpledialog.askstring("Delete Node", "Enter node name to delete:")
        if not node_name:
            return

        # Buscar y eliminar el nodo
        node_to_delete = None
        for node in self.current_graph.nodes:
            if node.name == node_name:
                node_to_delete = node
                break

        if not node_to_delete:
            messagebox.showerror("Error", f"Node '{node_name}' not found")
            return

        # Eliminar segmentos relacionados
        segments_to_keep = []
        for seg in self.current_graph.segments:
            if seg.origin != node_to_delete and seg.destination != node_to_delete:
                segments_to_keep.append(seg)

        self.current_graph.segments = segments_to_keep

        # Eliminar el nodo
        self.current_graph.nodes.remove(node_to_delete)

        # Actualizar listas de vecinos en otros nodos
        for node in self.current_graph.nodes:
            if node_to_delete in node.neighbors:
                node.neighbors.remove(node_to_delete)

        self.plot_current_graph()
        messagebox.showinfo("Success", f"Node '{node_name}' and related segments deleted")

    def create_new_graph(self):
        self.current_graph = Graph()
        self.plot_current_graph()
        messagebox.showinfo("Info", "New empty graph created")

    def save_graph_to_file(self):
        if not self.current_graph or not self.current_graph.nodes:
            messagebox.showwarning("Warning", "No graph to save")
            return

        filename = filedialog.asksaveasfilename(title="Save Graph",
                                                defaultextension=".txt",
                                                filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        if filename:
            if SaveGraphToFile(self.current_graph, filename):
                messagebox.showinfo("Success", "Graph saved successfully")
            else:
                messagebox.showerror("Error", "Failed to save graph")



def show_shortest_path(self):
    if not self.current_graph or len(self.current_graph.nodes) < 2:
        messagebox.showwarning("Warning", "Not enough nodes in graph")
        return

    origin = tk.simpledialog.askstring("Shortest Path", "Enter origin node name:")
    if not origin:
        return

    destination = tk.simpledialog.askstring("Shortest Path", "Enter destination node name:")
    if not destination:
        return

    path = FindShortestPath(self.current_graph, origin, destination)
    if path:
        messagebox.showinfo("Shortest Path", f"Path found with cost {path.cost:.1f}:\n{' -> '.join([node.name for node in path.nodes])}")
        self.plot_path(path)
    else:
        messagebox.showinfo("Shortest Path", "No path exists between these nodes")

def plot_path(self, path):
    self.ax.clear()

    # Dibujar todos los segmentos en gris primero
    for seg in self.current_graph.segments:
        self.ax.plot([seg.origin.x, seg.destination.x],
                     [seg.origin.y, seg.destination.y],
                     'gray', linewidth=1, alpha=0.3)

    # Resaltar segmentos del camino más corto
    for i in range(len(path.nodes)-1):
        origin = path.nodes[i]
        destination = path.nodes[i+1]
        self.ax.plot([origin.x, destination.x],
                     [origin.y, destination.y],
                     'r-', linewidth=2)
        # Mostrar costo en rojo
        mid_x = (origin.x + destination.x) / 2
        mid_y = (origin.y + destination.y) / 2
        self.ax.text(mid_x, mid_y, f"{Distance(origin, destination):.1f}",
                     fontsize=8, ha='center', va='center', color='red',
                     bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))

    # Dibujar nodos
    for node in self.current_graph.nodes:
        if node in path.nodes:
            color = 'blue' if node == path.nodes[0] or node == path.nodes[-1] else 'green'
        else:
            color = 'gray'

        self.ax.plot(node.x, node.y, 'o', markersize=10, color=color)
        self.ax.text(node.x, node.y, node.name,
                     fontsize=12, ha='center', va='center', color='white')

    self.ax.grid(True)
    self.ax.set_title(f"Shortest Path from {path.nodes[0].name} to {path.nodes[-1].name}")
    self.canvas.draw()

from path import *

def FindShortestPath(g, origin_name, destination_name):
    # Encontrar nodos de origen y destino
    origin = None
    destination = None
    for node in g.nodes:
        if node.name == origin_name:
            origin = node
        if node.name == destination_name:
            destination = node

    if origin is None or destination is None:
        return None

    # Implementación del algoritmo A*
    open_paths = [Path([origin], 0)]
    visited = set()

    while open_paths:
        # Encontrar el camino con el menor costo estimado
        current_path = min(open_paths, key=lambda p: p.cost + Distance(p.nodes[-1], destination))
        open_paths.remove(current_path)
        last_node = current_path.nodes[-1]

        # Si hemos llegado al destino
        if last_node == destination:
            return current_path

        # Marcar el nodo como visitado
        if last_node in visited:
            continue
        visited.add(last_node)

        # Expandir a los vecinos
        for neighbor in last_node.neighbors:
            if neighbor not in visited:
                # Encontrar el segmento correspondiente
                segment = None
                for seg in g.segments:
                    if seg.origin == last_node and seg.destination == neighbor:
                        segment = seg
                        break

                if segment:
                    new_path = AddNodeToPath(current_path, neighbor, segment.cost)
                    open_paths.append(new_path)

    return None  # No se encontró camino

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphApp(root)
    root.geometry("900x600")
    root.mainloop()

