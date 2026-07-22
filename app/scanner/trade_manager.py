from dataclasses import dataclass

@dataclass
class TradeResult:
    symbol: str
    status: str
    entry: float
    stop_loss: float
    target1: float
    target2: float
    current_price: float
    pnl_percent: float
    trailing_stop: float

class TradeManager:
    def __init__(self):
        pass

    def update(
        self,
        symbol,
        entry,
        stop_loss,
        target1,
        target2,
        current_price,
    ):
        pnl = ((current_price - entry) / entry) * 100
        trailing = stop_loss
        status = "OPEN"

        # 1. Evaluate Target progressions
        if current_price >= target1:
            trailing = entry
            status = "TARGET1_HIT"
            
        if current_price >= target2:
            trailing = target1
            status = "TARGET2_HIT"

        # 2. Evaluate if Stop Loss or Trailing Stop Loss is triggered
        if current_price <= trailing:
            status = "SL_EXIT" if trailing == stop_loss else "TRAILING_SL_EXIT"

        return TradeResult(
            symbol=symbol,
            status=status,
            entry=entry,
            stop_loss=stop_loss,
            target1=target1,
            target2=target2,
            current_price=current_price,
            pnl_percent=round(pnl, 2),
            trailing_stop=round(trailing, 2),
        )
