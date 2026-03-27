import sqlalchemy
import sqlalchemy.orm

@app.get("/stats")
def stats():
    return {"free":10,"pro":5}
@app.get("/validar")
def validar():
    return {"status":"ok"}

DATABASE_URL = "sqlite:///./aurexa.db"

engine = sqlalchemy.create_engine(DATABASE_URL)
SessionLocal = sqlalchemy.orm.sessionmaker(bind=engine)

Base = sqlalchemy.orm.declarative_base()
