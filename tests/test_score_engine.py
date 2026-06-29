from app.ai.score_engine import ScoreEngine

engine = ScoreEngine()

scores = {

    "market":20,

    "sector":15,

    "trend":15,

    "ema":15,

    "volume":10,

    "daily":10,

    "4h":10,

    "2h":10,

    "risk":5

}

result = engine.calculate(scores)

print(result)
