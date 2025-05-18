from airSpace import airSpace
from navPoint import navPoint
def test_load_files():
    airspace = airSpace()
    airspace.load_from_files('Cat_nav.txt', 'Cat_seg.txt', 'Cat_aer.txt')

    # Chequeo básico de que se cargaron datos
    assert len(airspace.navpoints) > 0
    assert len(airspace.navsegments) > 0
    assert len(airspace.navairports) > 0

    # Prueba de obtener un navpoint por nombre
    example_name = next(iter(airspace.navpoints.values())).name
    np = airspace.get_navpoint_by_name(example_name)
    assert np is not None
    assert np.name == example_name

    # Prueba obtener vecinos
    neighbors = airspace.get_neighbors(np)
    assert isinstance(neighbors, list)

    # Prueba buscar aeropuerto
    example_airport_name = next(iter(airspace.navairports.keys()))
    airport = airspace.find_airport(example_airport_name)
    assert airport is not None
    assert airport.name == example_airport_name

if __name__ == "__main__":
    test_load_files()
    print("test_airSpace passed")

def test_reachability():
    airspace = airSpace()
    airspace.load_from_files("Cat_nav.txt", "Cat_seg.txt", "Cat_aer.txt")

    origin = airspace.get_navpoint_by_name("GODOX")  # usa un nombre válido del archivo
    reachable = airspace.get_reachable_from(origin)

    assert isinstance(reachable, list)
    assert origin in reachable
    assert all(isinstance(n, navPoint) for n in reachable)

    print(f"Reachable from {origin.name}: {[n.name for n in reachable]}")