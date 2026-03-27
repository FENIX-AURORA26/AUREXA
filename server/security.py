from passlib.context import CryptContext

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_senha(senha):
return pwd.hash(senha)

def verificar_senha(senha, hash):
return pwd.verify(senha, hash)
