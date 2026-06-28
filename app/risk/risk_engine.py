from dataclasses import dataclass


@dataclass
class RiskResult:
    capital: float
    risk_percent: float
    risk_amount: float
    entry: float
    stop_loss: float
    risk_per_share: float
    quantity: int


class RiskEngine:

    def __init__(self, capital: float, risk_percent: float):

        self.capital = capital

        self.risk_percent = risk_percent

    def calculate(self, entry: float, stop_loss: float):

        risk_amount = self.capital * self.risk_percent / 100

        risk_per_share = abs(entry - stop_loss)

        if risk_per_share <= 0:
            raise ValueError("Invalid Stop Loss")

        quantity = int(risk_amount / risk_per_share)

        return RiskResult(

            capital=self.capital,

            risk_percent=self.risk_percent,

            risk_amount=round(risk_amount,2),

            entry=entry,

            stop_loss=stop_loss,

            risk_per_share=round(risk_per_share,2),

            quantity=max(quantity,1)

        )
