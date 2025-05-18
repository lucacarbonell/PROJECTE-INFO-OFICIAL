class navAirport:
    def __init__(self, name, sids=None, stars=None):

        self.name = name
        self.sids = sids if sids is not None else []
        self.stars = stars if stars is not None else []

    def add_sid(self, navpoint):
        self.sids.append(navpoint)

    def add_star(self, navpoint):
        self.stars.append(navpoint)

    def _repr_(self):
        return (f"NavAirport('{self.name}', "
                f"SIDs={[p.name for p in self.sids]}, "
                f"STARs={[p.name for p in self.stars]})")