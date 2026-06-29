class ScannerPipeline:

    def __init__(self):

        self.steps = [

            "Market",

            "Sector",

            "Trend",

            "EMA Pullback",

            "Volume",

            "Candlestick",

            "Multi Timeframe",

            "AI",

            "Risk"

        ]

    def run(self):

        return self.steps
