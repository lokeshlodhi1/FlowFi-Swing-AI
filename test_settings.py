from config.settings import settings

print(settings.get("capital"))

print(settings.get("ema", "fast"))

print(settings.get("risk", "risk_per_trade"))
