from dataclasses import dataclass


@dataclass
class AIConfidenceResult:

    confidence: int

    trade_grade: str

    recommendation: str

    passed: bool


class AIConfidenceEngine:

    def __init__(

        self,

        market_score,

        stock_score,

        strategy_confidence,

        risk_reward,

        relative_strength,

    ):

        self.market = market_score

        self.stock = stock_score

        self.strategy = strategy_confidence

        self.rr = risk_reward

        self.rs = relative_strength

    def evaluate(self):

        score = 0

        # -----------------------------
        # Market
        # -----------------------------

        score += self.market * 0.20

        # -----------------------------
        # Stock Quality
        # -----------------------------

        score += self.stock * 0.20

        # -----------------------------
        # Strategy
        # -----------------------------

        score += self.strategy * 0.30

        # -----------------------------
        # Relative Strength
        # -----------------------------

        score += self.rs * 0.20

        # -----------------------------
        # Risk Reward
        # -----------------------------

        score += min(self.rr * 10, 10)

        score = round(score)

        if score >= 90:

            return AIConfidenceResult(

                confidence=score,

                trade_grade="A+",

                recommendation="STRONG BUY",

                passed=True,

            )

        elif score >= 80:

            return AIConfidenceResult(

                confidence=score,

                trade_grade="A",

                recommendation="BUY",

                passed=True,

            )

        elif score >= 70:

            return AIConfidenceResult(

                confidence=score,

                trade_grade="B",

                recommendation="WATCH",

                passed=True,

            )

        return AIConfidenceResult(

            confidence=score,

            trade_grade="C",

            recommendation="REJECT",

            passed=False,

        )