import os
from uuid import uuid4
import httpx, psycopg
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field
from prometheus_fastapi_instrumentator import Instrumentator
app=FastAPI(title="Orders API")
Instrumentator().instrument(app).expose(app)
class Item(BaseModel): product_id:int; quantity:int=Field(gt=0,le=10)
class Request(BaseModel): customer_email:EmailStr; items:list[Item]=Field(min_length=1); payment_token:str
@app.get("/health")
def health(): return {"status":"ok"}
@app.post("/orders",status_code=201)
def create(req:Request):
    with psycopg.connect(os.environ["DATABASE_URL"]) as db:
        products=[]
        for item in req.items:
            row=db.execute("SELECT id,name,price_cents,stock FROM products WHERE id=%s",(item.product_id,)).fetchone()
            if not row: raise HTTPException(404,"Product not found")
            if row[3]<item.quantity: raise HTTPException(409,"Insufficient stock")
            products.append((row,item.quantity))
        total=sum(row[2]*qty for row,qty in products); order_id=str(uuid4())
        try:
            payment=httpx.post(os.getenv("PAYMENT_URL","http://payments:8000")+"/charge",json={"order_id":order_id,"amount_cents":total,"payment_token":req.payment_token},timeout=5).json()
        except httpx.HTTPError: raise HTTPException(502,"Payment service unavailable")
        status="paid" if payment["status"]=="paid" else "payment_failed"
        db.execute("INSERT INTO orders(id,customer_email,total_cents,status,payment_id) VALUES(%s,%s,%s,%s,%s)",(order_id,req.customer_email,total,status,payment.get("payment_id")))
        for row,qty in products:
            db.execute("INSERT INTO order_items VALUES(%s,%s,%s,%s,%s)",(order_id,row[0],row[1],qty,row[2]))
            if status=="paid": db.execute("UPDATE products SET stock=stock-%s WHERE id=%s",(qty,row[0]))
    return {"id":order_id,"status":status,"total_cents":total,"payment_id":payment.get("payment_id"),"message":payment.get("message")}
@app.get("/orders/{order_id}")
def get_order(order_id:str):
    with psycopg.connect(os.environ["DATABASE_URL"]) as db:
        row=db.execute("SELECT id,customer_email,total_cents,status,payment_id,created_at FROM orders WHERE id=%s",(order_id,)).fetchone()
        if not row: raise HTTPException(404,"Order not found")
        items=db.execute("SELECT product_id,product_name,quantity,unit_price_cents FROM order_items WHERE order_id=%s",(order_id,)).fetchall()
    return {"id":str(row[0]),"customer_email":row[1],"total_cents":row[2],"status":row[3],"payment_id":row[4],"created_at":row[5].isoformat(),"items":[dict(product_id=x[0],name=x[1],quantity=x[2],unit_price_cents=x[3]) for x in items]}
