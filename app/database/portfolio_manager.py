from .portfolio import Portfolio


class PortfolioManager:

    def __init__(self, capital=100000):

        self.capital = capital

    def build(

        self,

        invested,

        unrealized,

        realized,

        total,

        open_positions

    ):

        return Portfolio(

            capital=self.capital,

            invested=invested,

            available=self.capital - invested,

            unrealized_pnl=unrealized,

            realized_pnl=realized,

            total_trades=total,

            open_positions=open_positions

        )
