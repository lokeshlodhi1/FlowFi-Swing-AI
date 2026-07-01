from app.market.market_engine import MarketEngine
from app.scanner.stock_filter import StockFilter
from app.scanner.entry_engine import EntryEngine


class ScannerPipeline:

    def __init__(self):

        self.market_engine = MarketEngine()

    def analyse_stock(

        self,

        dataframe,

        price,

        avg_volume,

        delivery,

        market_cap,

        atr_percent,

        relative_strength,

    ):

        # ------------------------------------
        # STEP 1
        # Market Check
        # ------------------------------------

        market = self.market_engine.analyse_market()

        if not market["buy_allowed"]:

            return {

                "signal": "NO_SCAN",

                "reason": "Market Filter Failed"

            }

        # ------------------------------------
        # STEP 2
        # Stock Filter
        # ------------------------------------

        stock = StockFilter(

            price,

            avg_volume,

            delivery,

            market_cap,

            atr_percent,

            relative_strength,

        ).evaluate()

        if not stock.passed:

            return {

                "signal": "REJECT",

                "reason": stock.reason,

                "score": stock.score,

            }

        # ------------------------------------
        # STEP 3
        # Entry Engine
        # ------------------------------------

        entry = EntryEngine(

            dataframe

        ).analyse()

        return {

            "signal": entry["signal"],

            "strategy": entry["strategy"],

            "confidence": entry["confidence"],

            "entry": entry["entry"],

            "stop_loss": entry["stop_loss"],

            "target1": entry["target1"],

            "target2": entry["target2"],

            "risk_reward": entry["risk_reward"],

            "stock_score": stock.score,

            "reason": entry["reason"],

        }