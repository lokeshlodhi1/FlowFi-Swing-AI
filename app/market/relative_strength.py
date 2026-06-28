class RelativeStrengthEngine:

    def __init__(self):

        pass

    def calculate(

        self,

        stock_change,

        market_change

    ):

        rs = stock_change - market_change

        return round(rs,2)

    def grade(self, rs):

        if rs >= 10:

            return "Excellent"

        elif rs >= 5:

            return "Strong"

        elif rs >= 0:

            return "Average"

        else:

            return "Weak"
