from app.ai.decision_engine import DecisionEngine

features = {
    "market": 100,
    "sector": 95,
    "ema": 100,
    "volume": 90,
    "relative_strength": 92,
    "candlestick": 85,
    "timeframe": 100
}

engine = DecisionEngine()

print(engine.score(features))
