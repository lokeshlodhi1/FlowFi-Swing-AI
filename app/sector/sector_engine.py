class SectorEngine:

    def __init__(self, sector_data):

        self.sector_data = sector_data

    def rank(self):

        ranked = sorted(

            self.sector_data.items(),

            key=lambda x: x[1],

            reverse=True

        )

        return ranked

    def top(self, n=5):

        return self.rank()[:n]

    def bottom(self, n=5):

        return self.rank()[-n:]

    def strength(self, sector):

        return self.sector_data.get(sector, 0)
