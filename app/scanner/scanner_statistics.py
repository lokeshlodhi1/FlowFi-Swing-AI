from collections import defaultdict


class ScannerStatistics:

    def __init__(self):
        self.data = defaultdict(int)

    def add(self, reason):
        self.data[reason] += 1

    def report(self):

        print("\n" + "=" * 70)
        print("SCANNER DIAGNOSTICS")
        print("=" * 70)

        total = sum(self.data.values())

        print(f"Total Checked : {total}")
        print()

        for reason, count in sorted(self.data.items()):
            print(f"{reason:<35} {count}")

        print("=" * 70)
