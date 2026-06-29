from dataclasses import dataclass
from datetime import datetime

import pandas as pd


@dataclass(slots=True)
class MarketData:
    symbol: str
    timeframe: str
    data: pd.DataFrame
    downloaded_at: datetime

    @property
    def rows(self):

        return len(self.data)

    @property
    def empty(self):

        return self.data.empty
