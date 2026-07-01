from dataclasses import dataclass
from datetime import datetime


@dataclass
class JournalEntry:

    symbol: str

    strategy: str

    entry: float

    stop_loss: float

    target1: float

    target2: float

    quantity: int

    status: str

    pnl: float

    created_at: str


class TradeJournal:

    def __init__(self):

        self.trades = []

    def add_trade(

        self,

        symbol,

        strategy,

        entry,

        stop_loss,

        target1,

        target2,

        quantity,

    ):

        self.trades.append(

            JournalEntry(

                symbol=symbol,

                strategy=strategy,

                entry=entry,

                stop_loss=stop_loss,

                target1=target1,

                target2=target2,

                quantity=quantity,

                status="OPEN",

                pnl=0,

                created_at=datetime.now().strftime(

                    "%Y-%m-%d %H:%M:%S"

                ),

            )

        )

    def close_trade(

        self,

        symbol,

        exit_price,

    ):

        for trade in self.trades:

            if (

                trade.symbol == symbol

                and

                trade.status == "OPEN"

            ):

                trade.status = "CLOSED"

                trade.pnl = round(

                    (exit_price - trade.entry)

                    * trade.quantity,

                    2,

                )

                return trade

        return None

    def get_open_trades(self):

        return [

            trade

            for trade in self.trades

            if trade.status == "OPEN"

        ]

    def get_closed_trades(self):

        return [

            trade

            for trade in self.trades

            if trade.status == "CLOSED"

        ]