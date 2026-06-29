from .score_weights import SCORE_WEIGHTS, MAX_SCORE
from .score_result import ScoreResult


class ScoreEngine:

    def calculate(self, scores: dict):

        total = sum(scores.values())

        confidence = round(total / MAX_SCORE * 100, 2)

        if confidence >= 90:

            signal = "BUY"

        elif confidence >= 75:

            signal = "WATCH"

        else:

            signal = "IGNORE"

        return ScoreResult(

            total=total,

            confidence=confidence,

            signal=signal,

            passed=confidence >= 90

        )
