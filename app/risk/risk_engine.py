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
    position_value: float
    max_loss: float
    target1: float
    target2: float
    risk_reward: float
    valid: bool
    reason: str


class RiskEngine:

    def __init__(self, capital: float, risk_percent: float = 1.0):

        self.capital = capital
        self.risk_percent = risk_percent

    def calculate(
        self,
        entry: float,
        stop_loss: float,
        target1: float,
        target2: float,
    ):

        risk_amount = self.capital * self.risk_percent / 100

        risk_per_share = abs(entry - stop_loss)

        if risk_per_share <= 0:

            return RiskResult(
                capital=self.capital,
                risk_percent=self.risk_percent,
                risk_amount=0,
                entry=entry,
                stop_loss=stop_loss,
                risk_per_share=0,
                quantity=0,
                position_value=0,
                max_loss=0,
                target1=target1,
                target2=target2,
                risk_reward=0,
                valid=False,
                reason="Invalid Stop Loss",
            )

        quantity = max(int(risk_amount / risk_per_share), 1)

        position_value = quantity * entry

        max_loss = quantity * risk_per_share

        reward = target1 - entry

        rr = round(reward / risk_per_share, 2)

        valid = rr >= 2

        reason = "Risk Accepted"

        if not valid:
            reason = "Risk Reward Below 1:2"

        return RiskResult(

            capital=self.capital,

            risk_percent=self.risk_percent,

            risk_amount=round(risk_amount, 2),

            entry=round(entry, 2),

            stop_loss=round(stop_loss, 2),

            risk_per_share=round(risk_per_share, 2),

            quantity=quantity,

            position_value=round(position_value, 2),

            max_loss=round(max_loss, 2),

            target1=round(target1, 2),

            target2=round(target2, 2),

            risk_reward=rr,

            valid=valid,

            reason=reason,

        )