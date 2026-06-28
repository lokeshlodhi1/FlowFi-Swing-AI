class MultiTimeframeEngine:

    def __init__(self):
        pass

    def confirm(
        self,
        daily_signal: str,
        four_hour_signal: str,
        two_hour_signal: str
    ) -> dict:

        score = 0

        if daily_signal == four_hour_signal:
            score += 40

        if four_hour_signal == two_hour_signal:
            score += 30

        if daily_signal == two_hour_signal:
            score += 30

        if score == 100:
            status = "CONFIRMED"

        elif score >= 70:
            status = "PARTIAL"

        else:
            status = "REJECT"

        return {

            "status": status,

            "score": score

        }
