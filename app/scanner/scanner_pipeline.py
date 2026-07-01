from app.market.market_engine import MarketEngine
from app.scanner.relative_strength import RelativeStrength
from app.scanner.stock_quality import StockQuality


class ScannerPipeline:

    def __init__(self):

        self.market_engine = MarketEngine()

        self.steps = [

            "Market Filter",

            "Relative Strength",

            "Stock Quality",

            "Entry Engine",

            "Risk Engine",

            "AI Decision",

            "Telegram Signal"

        ]

    def get_pipeline(self):
        return self.steps

    def analyse_stock(

        self,

        stock_close,

        market_close,

        liquidity_score,

        volume_score,

        atr_score,

        delivery_score,

        market_cap_score,

    ):

        # STEP 1
        market = self.market_engine.analyse_market()

        if not market["buy_allowed"]:

            return {

                "signal": "NO_SCAN",

                "reason": "Market not suitable",

                "market": market

            }

        # STEP 2
        rs = RelativeStrength(

            stock_close,

            market_close

        ).calculate()

        # STEP 3
        quality = StockQuality(

            rs.score,

            liquidity_score,

            volume_score,

            atr_score,

            delivery_score,

            market_cap_score

        ).evaluate()

        # STEP 4
        if quality.score >= 90:

            signal = "BUY"

        elif quality.score >= 75:

            signal = "WATCH"

        else:

            signal = "REJECT"

        return {

            "signal": signal,

            "market": market,

            "relative_strength": rs,

            "quality": quality

        }