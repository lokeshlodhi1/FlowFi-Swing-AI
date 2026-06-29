import os

import matplotlib.pyplot as plt


class ChartGenerator:

    def generate(self, df, symbol):

        plt.figure(figsize=(12, 6))

        plt.plot(df["Close"], label="Close")

        if "EMA20" in df.columns:
            plt.plot(df["EMA20"], label="EMA20")

        if "EMA50" in df.columns:
            plt.plot(df["EMA50"], label="EMA50")

        if "EMA200" in df.columns:
            plt.plot(df["EMA200"], label="EMA200")

        plt.title(symbol)

        plt.legend()

        os.makedirs("charts", exist_ok=True)

        filename = f"charts/{symbol}.png"

        plt.savefig(filename)

        plt.close()

        return filename
