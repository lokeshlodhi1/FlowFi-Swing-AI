from .trade_signal import TradeSignal


class TradeBuilder:

    def build(

        self,

        symbol,

        confidence,

        entry,

        stop,

        quantity,

        reasons

    ):

        risk = entry - stop

        target1 = round(entry + risk * 2, 2)

        target2 = round(entry + risk * 3, 2)

        rr = round((target2 - entry) / risk, 2)

        return TradeSignal(

            symbol=symbol,

            signal="BUY",

            confidence=confidence,

            entry=round(entry, 2),

            stop_loss=round(stop, 2),

            target1=target1,

            target2=target2,

            quantity=quantity,

            risk_reward=rr,

            reasons=reasons

        )
