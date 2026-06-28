class TargetEngine:

    def calculate(self, entry, stop):

        risk = entry - stop

        return {

            "Target1": round(entry + risk * 2, 2),

            "Target2": round(entry + risk * 3, 2),

            "Target3": "Trail EMA20"

        }
