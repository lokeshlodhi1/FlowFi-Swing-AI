# FlowFi AI Swing Trading Strategy v1

## Objective

Identify high-probability swing trades in NSE stocks using trend, pullback, volume, and multi-timeframe confirmation.

---

## Market Filter

- Nifty trend must agree.
- Bank Nifty trend must agree.
- If market is bullish → BUY only.
- If market is bearish → SELL only.

---

## Sector Filter

- Buy only from the Top 5 strongest sectors.
- Sell only from the Bottom 5 weakest sectors.

---

## Stock Filter

Reject:

- Price below ₹100
- Low liquidity
- Low traded value
- F&O ban (future)
- Corporate action (future)

---

## Trend

BUY

EMA20 > EMA50 > EMA200

SELL

EMA20 < EMA50 < EMA200

---

## Pullback

Price should retrace near EMA20.

No chasing.

---

## Volume

Relative Volume > 1.5

Average Daily Traded Value above minimum threshold.

---

## Daily Confirmation

Accepted patterns

- Bullish Engulfing
- Hammer
- Marubozu

---

## Multi Timeframe

Daily

↓

4H

↓

2H

All must agree.

---

## Entry

Buy above confirmation candle high.

Sell below confirmation candle low.

---

## Stop Loss

ATR

OR

Swing Low

Whichever is safer.

---

## Targets

Target 1 = 2R

Target 2 = 3R

Remaining quantity trails using EMA20.

---

## Risk

Maximum risk

1%

Maximum open trades

5

---

## AI Score

Minimum score = 90

Below 90

Ignore.

---

## Telegram Alert

Send

- Stock
- Entry
- Stop Loss
- Targets
- Quantity
- AI Score
- Reasons
- Chart
