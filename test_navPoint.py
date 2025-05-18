from navPoint import navPoint

def test_navpoint_creation():
    np = navPoint(123, "TEST", 41.5, 2.2)
    assert np.number == 123
    assert np.name == "TEST"
    assert abs(np.latitude - 41.5) < 1e-6
    assert abs(np.longitude - 2.2) < 1e-6

def test_distance_to():
    np1 = navPoint(1, "A", 0.0, 0.0)
    np2 = navPoint(2, "B", 3.0, 4.0)
    dist = np1.distance_to(np2)
    assert abs(dist - 5.0) < 1e-6

if __name__ == "__main__":
    test_navpoint_creation()
    test_distance_to()
    print("test_navPoint passed")