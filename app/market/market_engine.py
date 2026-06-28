import pandas as pd


class MarketEngine:

    def __init__(self, nifty_df, bank_df):

        self.nifty = nifty_df

        self.bank = bank_df

    def market_trend(self):

        n = self.nifty.iloc[-1]

        b = self.bank.iloc[-1]

        nifty_bull = (

            n["EMA20"]

            >

            n["EMA50"]

            >

            n["EMA200"]

        )

        bank_bull = (

            b["EMA20"]

            >

            b["EMA50"]

            >

            b["EMA200"]

        )

        if nifty_bull and bank_bull:

            return {

                "Market": "Bullish",

                "Trade": "BUY"

            }

        if (not nifty_bull) and (not bank_bull):

            return {

                "Market": "Bearish",

                "Trade": "SELL"

            }

        return {

            "Market": "Neutral",

            "Trade": "WAIT"

        }
