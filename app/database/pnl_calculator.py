class PnlCalculator:

    def unrealized(

        self,

        entry,

        current,

        quantity

    ):

        return round(

            (current - entry) * quantity,

            2

        )

    def realized(

        self,

        entry,

        exit_price,

        quantity

    ):

        return round(

            (exit_price - entry) * quantity,

            2

        )
