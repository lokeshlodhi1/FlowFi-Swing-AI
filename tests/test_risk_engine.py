from app.risk.risk_engine import RiskEngine

engine = RiskEngine(

    capital=100000,

    risk_percent=1

)

result = engine.calculate(

    entry=425.60,

    stop_loss=414.20

)

print(result)
