from collections import defaultdict


class ScannerStatistics:

    def __init__(self):
        self.stats = defaultdict(int)

    def add(self, reason):
        self.stats[reason] += 1

    def report(self):

        print("\n" + "=" * 60)
        print("SCANNER STATISTICS")
        print("=" * 60)

        for key, value in sorted(self.stats.items()):
            print(f"{key:<30} : {value}")

        print("=" * 60)
