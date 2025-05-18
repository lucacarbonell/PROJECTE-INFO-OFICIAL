from airSpace import airSpace
from path import a_star

def test_shortest_path():
    airspace = airSpace()
    airspace.load_from_files("Cat_nav.txt", "Cat_seg.txt", "Cat_aer.txt")

    # Cambia estos valores por nombres reales de puntos de tu fichero
    origin = airspace.get_navpoint_by_name("GODOX")
    destination = airspace.get_navpoint_by_name("SUKET")

    if origin is None or destination is None:
        print("Error: origen o destino no encontrados.")
        return

    result = a_star(airspace, origin, destination)

    if result:
        print("Camino más corto encontrado:")
        for p in result.points:
            print(p.name, end=" → ")
        print(f"\nCoste total: {result.cost:.2f} km")
    else:
        print("No se encontró ningún camino.")

if __name__ == "__main__":
    test_shortest_path()