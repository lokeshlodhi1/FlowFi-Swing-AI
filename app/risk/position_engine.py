class PositionEngine:

    def calculate(self, capital, quantity, entry):

        invested = quantity * entry

        exposure = (invested / capital) * 100

        return {

            "invested": round(invested, 2),

            "exposure": round(exposure, 2)

        }
