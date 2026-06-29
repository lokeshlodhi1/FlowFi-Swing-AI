import pandas as pd


class DataValidator:

    REQUIRED_COLUMNS = [

        "Open",

        "High",

        "Low",

        "Close",

        "Volume"

    ]

    def validate(self, df: pd.DataFrame):

        if df.empty:
            return False

        for column in self.REQUIRED_COLUMNS:

            if column not in df.columns:
                return False

        if df.isna().sum().sum() > 0:
            return False

        return True
