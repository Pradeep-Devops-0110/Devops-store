from uuid import uuid4
from fastapi import FastAPI
from pydantic import BaseModel,Field
from prometheus_fastapi_instrumentator import Instrumentator
app=FastAPI(title="Simulated Payments API")
Instrumentator().instrument(app).expose(app)
class Charge(BaseModel):
    order_id:str
    amount_cents:int=Field(gt=0)
    payment_token:str
@app.get("/health")
def health(): return {"status":"ok","mode":"simulated"}
@app.post("/charge")
def charge(c:Charge):
    if c.payment_token.lower()=="fail": return {"status":"declined","payment_id":None,"message":"Simulated decline"}
    return {"status":"paid","payment_id":"pay_"+uuid4().hex[:12],"message":"Simulated payment approved"}
