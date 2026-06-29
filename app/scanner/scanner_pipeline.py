class ScannerPipeline:

    def __init__(self):

        self.steps = [

    "Market Filter",

    "Trend Filter",

    "EMA Pullback",

    "Volume Confirmation",

    "Daily Confirmation",

    "4H Confirmation",

    "2H Confirmation",

    "AI Decision",

    "Risk Engine"

]

    def run(self):

        return self.steps
