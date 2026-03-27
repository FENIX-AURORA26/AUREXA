from fastapi import FastAPI
from pydantic import BaseModel
import stripe
import jwt
from datetime import datetime, timedelta
from database import engine
from models import Base
Base.metadata.create_all(bind=engine)
app = FastAPI()
stripe.api_key = "SUA_SECRET_KEY"
SECRET = "AUREXA_SECRET"
class LoginData(BaseModel):
email:str
senha:str
@app.post("/login")
def login(data: LoginData):
if data.email == "[admin@aurexa.com](mailto:admin@aurexa.com)" and data.senha == "123":
token = jwt.encode({
"user": data.email,
"exp": datetime.utcnow() + timedelta(days=30)
}, SECRET, algorithm="HS256")
return {"token": token}
return {"erro":"login inválido"}
@app.post("/create-checkout-session")
def checkout():
session = stripe.checkout.Session.create(
payment_method_types=['card'],
line_items=[{
'price_data': {
'currency': 'brl',
'product_data': {'name': 'AUREXA PRO'},
'unit_amount': 2990,
},
'quantity': 1,
}],
mode='payment',
success_url='http://localhost:5500/sucesso.html',
cancel_url='http://localhost:5500/cancelado.html',
)
return {"id": session.id}
