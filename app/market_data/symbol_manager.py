from pathlib import Path
import json


class SymbolManager:
    """
    Loads stock symbols from watchlists.
    """

    def __init__(self, watchlist_dir: str = "watchlists"):
        self.watchlist_dir = Path(watchlist_dir)

    def load(self, universe: str):

        file = self.watchlist_dir / f"{universe.lower()}.json"

        if not file.exists():
            raise FileNotFoundError(file)

        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)

        return data["symbols"]

    def custom(self, filename: str):

        file = self.watchlist_dir / filename

        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)

        return data["symbols"]
