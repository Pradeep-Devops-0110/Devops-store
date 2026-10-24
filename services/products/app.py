import os
import psycopg
from fastapi import FastAPI
app=FastAPI(title="Products API")
@app.get("/health")
def health(): return {"status":"ok"}
@app.get("/products")
def products():
    with psycopg.connect(os.environ["DATABASE_URL"]) as db:
        rows=db.execute("SELECT id,name,description,price_cents,stock FROM products ORDER BY id").fetchall()
    return [dict(id=r[0],name=r[1],description=r[2],price_cents=r[3],stock=r[4]) for r in rows]
