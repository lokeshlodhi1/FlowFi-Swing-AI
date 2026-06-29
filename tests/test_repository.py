from app.database.database_service import DatabaseService

db = DatabaseService()

db.signals.add_signal(

    "BEL.NS",

    96,

    "BUY"

)

print(

    db.signals.all()

)
