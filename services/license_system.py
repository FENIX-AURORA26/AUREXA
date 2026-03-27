from datetime import datetime, timedelta
import jwt

SECRET = "AUREXA_SECRET_KEY"

def gerar_token(user_id):
payload = {
"user_id": user_id,
"exp": datetime.utcnow() + timedelta(days=30)
}
return jwt.encode(payload, SECRET, algorithm="HS256")

def validar_token(token):
try:
return jwt.decode(token, SECRET, algorithms=["HS256"])
except:
return None
