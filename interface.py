import tkinter as tk
from tkinter import filedialog, messagebox
from test_graph import *
from node import node

# Variable global per desar el gràfic actual
current_graph = None

# Funció per mostrar el gràfic d'exemple
def show_example_graph():
    global current_graph
    current_graph = CreateGraph_1()  # Desa el gràfic a la variable global
    Plot(current_graph)

# Funció per mostrar el gràfic inventat
def show_invented_graph():
    global current_graph
    current_graph = CreateGraph_2()  # Desa el gràfic a la variable global
    Plot(current_graph)

# Funció per carregar un gràfic des de fitxer
def load_graph_from_file():
    global current_graph
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if not file_path:
        return
    current_graph = Graph().CreateGraphFromFile(file_path)  # Desa el gràfic carregat
    Plot(current_graph)

# Funció per mostrar els veïns del node seleccionat en el gràfic actual
def show_neighbors():
    if current_graph is None:
        messagebox.showerror("Error", "Cap gràfic seleccionat.")
        return

    node_name = node_listbox.get(tk.ACTIVE)  # Obtenir el nom del node seleccionat
    node = next((n for n in current_graph.nodes if n.name == node_name), None)

    if node:
        # Crear un gràfic només amb el node seleccionat i els seus veïns
        fig, ax = plt.subplots()
        ax.scatter(node.x, node.y, color='blue')  # Dibuixar el node seleccionat
        ax.text(node.x, node.y, node.name, fontsize=12, verticalalignment='bottom')

        for neighbor in node.neighbors:
            ax.scatter(neighbor.x, neighbor.y, color='green')  # Dibuixar el veí
            ax.plot([node.x, neighbor.x], [node.y, neighbor.y], 'r-', linewidth=2)  # Dibuixar la connexió

            # Afegir la distància al centre del segment
            mid_x = (node.x + neighbor.x) / 2
            mid_y = (node.y + neighbor.y) / 2
            distance = current_graph.CalculateDistance(node, neighbor)
            ax.text(mid_x, mid_y, f"{distance:.2f}", fontsize=10, color='red')

        plt.xlabel("X")
        plt.ylabel("Y")
        plt.title(f"Veïns de {node_name}")
        plt.show()
    else:
        messagebox.showerror("Error", f"Node {node_name} no trobat en el gràfic actual.")

# Crear la finestra principal de Tkinter
root = tk.Tk()
root.title("Interfície de Gràfics")

# Crear els botons i components
example_button = tk.Button(root, text="Mostrar Gràfic Exemple", command=show_example_graph)
example_button.pack(pady=10)

invented_button = tk.Button(root, text="Mostrar Gràfic Inventat", command=show_invented_graph)
invented_button.pack(pady=10)

file_button = tk.Button(root, text="Carregar Gràfic des de fitxer", command=load_graph_from_file)
file_button.pack(pady=10)

# Crear llistat de nodes per seleccionar un node i veure els veïns
node_listbox = tk.Listbox(root)
node_listbox.pack(pady=10)

# Afegir nodes inicials a la llista (això es pot actualitzar quan es carregui un nou gràfic)
node_listbox.insert(tk.END, "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L")

# Crear botó per mostrar veïns d'un node seleccionat
neighbors_button = tk.Button(root, text="Mostrar Veïns", command=show_neighbors)
neighbors_button.pack(pady=10)

# Iniciar la interfície gràfica
root.mainloop()
