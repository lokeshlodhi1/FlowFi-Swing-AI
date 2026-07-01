from dataclasses import dataclass

from app.scanner.entry_engine import EntryEngine
from app.risk.risk_engine import RiskEngine


@dataclass
class TradingSignal:

    signal: str

    strategy: str

    confidence: int

    entry: float

    stop_loss: float

    target1: float

    target2: float

    quantity: int

    position_value: float

    risk_reward: float

    reason: str


class SignalGenerator:

    def __init__(

        self,

        capital,

        risk_percent=1.0,

    ):

        self.capital = capital

        self.risk_percent = risk_percent

    def generate(self, dataframe):

        entry_engine = EntryEngine(dataframe)

        result = entry_engine.analyse()

        if result["signal"] == "WATCH":

            return TradingSignal(

                signal="WATCH",

                strategy="NONE",

                confidence=0,

                entry=0,

                stop_loss=0,

                target1=0,

                target2=0,

                quantity=0,

                position_value=0,

                risk_reward=0,

                reason="No Valid Strategy"

            )

        risk = RiskEngine(

            self.capital,

            self.risk_percent

        ).calculate(

            result["entry"],

            result["stop_loss"],

            result["target1"],

            result["target2"]

        )

        if not risk.valid:

            return TradingSignal(

                signal="REJECT",

                strategy=result["strategy"],

                confidence=result["confidence"],

                entry=result["entry"],

                stop_loss=result["stop_loss"],

                target1=result["target1"],

                target2=result["target2"],

                quantity=0,

                position_value=0,

                risk_reward=risk.risk_reward,

                reason=risk.reason

            )

        return TradingSignal(

            signal=result["signal"],

            strategy=result["strategy"],

            confidence=result["confidence"],

            entry=result["entry"],

            stop_loss=result["stop_loss"],

            target1=result["target1"],

            target2=result["target2"],

            quantity=risk.quantity,

            position_value=risk.position_value,

            risk_reward=risk.risk_reward,

            reason="Trade Approved"

        )