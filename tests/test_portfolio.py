from app.database.portfolio_manager import PortfolioManager

portfolio = PortfolioManager(100000)

summary = portfolio.build(

    invested=35000,

    unrealized=2500,

    realized=1200,

    total=12,

    open_positions=3

)

print(summary)
