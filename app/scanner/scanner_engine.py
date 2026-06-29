from .scanner_pipeline import ScannerPipeline


class ScannerEngine:

    def __init__(self):

        self.pipeline = ScannerPipeline()

    def scan(self):

        print()

        print("========== FLOWFI AI SCANNER ==========")

        print()

        for step in self.pipeline.run():

            print(f"Running : {step}")

        print()

        print("Scanner Finished")
