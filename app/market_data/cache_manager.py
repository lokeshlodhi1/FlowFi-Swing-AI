from pathlib import Path
import pandas as pd


class CacheManager:

    def __init__(self, cache_dir="cache"):

        self.cache_dir = Path(cache_dir)

        self.cache_dir.mkdir(exist_ok=True)

    def save(self, symbol, interval, df):

        file = self.cache_dir / f"{symbol}_{interval}.parquet"

        df.to_parquet(file)

    def load(self, symbol, interval):

        file = self.cache_dir / f"{symbol}_{interval}.parquet"

        if not file.exists():
            return None

        return pd.read_parquet(file)

    def exists(self, symbol, interval):

        file = self.cache_dir / f"{symbol}_{interval}.parquet"

        return file.exists()

    def clear(self):

        for file in self.cache_dir.glob("*.parquet"):
            file.unlink()
