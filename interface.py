import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from test_graph import *
from node import node
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class GraphInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Interfície de Gràfics")
        self.root.geometry("800x600")

        self.graph = Graph()

        # Frame per mostrar el gràfic
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = None
        self.first_node = None  # Per afegir un segment

        # Botons
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=10)

        self.example_button = tk.Button(self.button_frame, text="Mostrar Gràfic Exemple",
                                        command=self.show_example_graph)
        self.example_button.grid(row=0, column=0, padx=5)

        self.invented_button = tk.Button(self.button_frame, text="Mostrar Gràfic Inventat",
                                         command=self.show_invented_graph)
        self.invented_button.grid(row=0, column=1, padx=5)

        self.file_button = tk.Button(self.button_frame, text="Carregar Gràfic des de fitxer",
                                     command=self.load_graph_from_file)
        self.file_button.grid(row=0, column=2, padx=5)

        self.neighbors_button = tk.Button(self.button_frame, text="Mostrar Veïns", command=self.show_neighbors)
        self.neighbors_button.grid(row=0, column=3, padx=5)

        self.add_node_button = tk.Button(self.button_frame, text="Afegir Node", command=self.add_node)
        self.add_node_button.grid(row=1, column=0, padx=5)

        self.add_segment_button = tk.Button(self.button_frame, text="Afegir Segment", command=self.add_segment)
        self.add_segment_button.grid(row=1, column=1, padx=5)

        self.delete_node_button = tk.Button(self.button_frame, text="Eliminar Node", command=self.delete_node)
        self.delete_node_button.grid(row=1, column=2, padx=5)

        self.save_graph_button = tk.Button(self.button_frame, text="Guardar Gràfic", command=self.save_graph)
        self.save_graph_button.grid(row=1, column=3, padx=5)

        self.design_graph_button = tk.Button(self.button_frame, text="Dissenyar Gràfic", command=self.design_graph)
        self.design_graph_button.grid(row=2, column=0, padx=5)

        # Llista de nodes
        self.node_listbox = tk.Listbox(self.root)
        self.node_listbox.pack(pady=5)

        # Afegim un event de clic per afegir nodes i segments interactius
        self.frame.bind("<Button-1>", self.add_node_interactive)

    def show_graph(self):
        if self.canvas:
            self.canvas.get_tk_widget().destroy()

        fig, ax = plt.subplots()

        for n in self.graph.nodes:
            ax.scatter(n.x, n.y, color='gray')
            ax.text(n.x, n.y, n.name, fontsize=12, verticalalignment='bottom')

        for seg in self.graph.segments:
            x_values = [seg.origin.x, seg.destination.x]
            y_values = [seg.origin.y, seg.destination.y]
            ax.plot(x_values, y_values, 'k--')

        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_title("Gràfic")

        self.canvas = FigureCanvasTkAgg(fig, master=self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

        self.node_listbox.delete(0, tk.END)
        for n in self.graph.nodes:
            self.node_listbox.insert(tk.END, n.name)

    def show_example_graph(self):
        self.graph = CreateGraph_1()
        self.show_graph()

    def show_invented_graph(self):
        self.graph = CreateGraph_2()
        self.show_graph()

    def load_graph_from_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if not file_path:
            return
        self.graph = Graph().CreateGraphFromFile(file_path)
        self.show_graph()

    def show_neighbors(self):
        if not self.graph:
            messagebox.showerror("Error", "Cap gràfic carregat")
            return

        node_name = self.node_listbox.get(tk.ACTIVE)
        node = next((n for n in self.graph.nodes if n.name == node_name), None)

        if not node:
            messagebox.showerror("Error", f"Node {node_name} no trobat.")
            return

        # Crear una nova figura dins de la mateixa finestra
        fig, ax = plt.subplots()
        ax.scatter(node.x, node.y, color='blue')
        ax.text(node.x, node.y, node.name, fontsize=12, verticalalignment='bottom')

        for neighbor in node.neighbors:
            ax.scatter(neighbor.x, neighbor.y, color='green')
            ax.plot([node.x, neighbor.x], [node.y, neighbor.y], 'r-', linewidth=2)

        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_title(f"Veïns de {node_name}")

        # Dibuixar el gràfic dins de la finestra principal
        if self.canvas:
            self.canvas.get_tk_widget().destroy()  # Eliminar el canvas anterior
        self.canvas = FigureCanvasTkAgg(fig, master=self.frame)  # Crear un nou canvas amb la figura
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()  # Mostrar-lo dins de la finestra principal

    def add_node(self):
        name = simpledialog.askstring("Afegir Node", "Nom del node:")
        x = simpledialog.askfloat("Afegir Node", "Coordenada X:")
        y = simpledialog.askfloat("Afegir Node", "Coordenada Y:")

        if name and x is not None and y is not None:
            self.graph.AddNode(node(name, x, y))
            self.show_graph()

    def add_segment(self):
        name = simpledialog.askstring("Afegir Segment", "Nom del segment:")
        origin = simpledialog.askstring("Afegir Segment", "Node origen:")
        destination = simpledialog.askstring("Afegir Segment", "Node destí:")

        if name and origin and destination:
            self.graph.AddSegment(name, origin, destination)
            self.show_graph()

    def delete_node(self):
        node_name = self.node_listbox.get(tk.ACTIVE)
        self.graph.nodes = [n for n in self.graph.nodes if n.name != node_name]
        self.graph.segments = [s for s in self.graph.segments if
                               s.origin.name != node_name and s.destination.name != node_name]
        self.show_graph()

    def save_graph(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, 'w') as f:
                f.write("Nodes:\n")
                for n in self.graph.nodes:
                    f.write(f"{n.name} {n.x} {n.y}\n")
                f.write("Segments:\n")
                for s in self.graph.segments:
                    f.write(f"{s.name} {s.origin.name} {s.destination.name}\n")

    def design_graph(self):
        """Permet dissenyar un gràfic des de zero."""
        self.graph = Graph().DesignGraph()
        self.show_graph()  # Actualitzar la vista del gràfic

    def add_node_interactive(self, event):
        """Afegir un node al fer clic al gràfic."""
        x = event.x
        y = event.y
        node_name = f"Node_{len(self.graph.nodes) + 1}"
        new_node = node(node_name, x, y)
        self.graph.AddNode(new_node)
        self.show_graph()

        # Si tenim un primer node seleccionat, afegim un segment
        if self.first_node:
            self.graph.AddSegment(f"{self.first_node.name}{new_node.name}", self.first_node.name, new_node.name)
            self.first_node = None  # Reiniciem el primer node per afegir un segment

        # Si no, guardem el primer node per afegir un segment posteriorment
        else:
            self.first_node = new_node


if __name__ == "__main__":
    root = tk.Tk()
    app = GraphInterface(root)
    root.mainloop()
