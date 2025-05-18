from navAirport import navAirport
from navPoint import navPoint

def test_navairport_creation():
    sids = [navPoint(1, "SID1.D", 41.0, 2.0)]
    stars = [navPoint(2, "STAR1.A", 40.5, 2.5)]
    airport = navAirport("TEST_AIRPORT", sids, stars)
    assert airport.name == "TEST_AIRPORT"
    assert len(airport.sids) == 1
    assert len(airport.stars) == 1
    assert airport.sids[0].name == "SID1.D"
    assert airport.stars[0].name == "STAR1.A"

def test_add_sid_star():
    airport = navAirport("TEST")
    sid = navPoint(3, "SID2.D", 41.2, 2.2)
    star = navPoint(4, "STAR2.A", 40.8, 2.8)
    airport.add_sid(sid)
    airport.add_star(star)
    assert airport.sids[0] == sid
    assert airport.stars[0] == star

if __name__ == "__main__":
    test_navairport_creation()
    test_add_sid_star()
    print("test_navAirport passed")