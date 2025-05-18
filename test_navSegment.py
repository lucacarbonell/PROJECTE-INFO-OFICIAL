from navSegment import navSegment

def test_navsegment_creation():
    seg = navSegment(1, 2, 10.5)
    assert seg.origin_number == 1
    assert seg.destination_number == 2
    assert abs(seg.distance - 10.5) < 1e-6

if __name__ == "__main__":
    test_navsegment_creation()
    print("test_navSegment passed")