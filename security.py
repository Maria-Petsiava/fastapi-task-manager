from datetime import datetime, timedelta, timezone
import jwt
from pwdlib import PasswordHash
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from database import get_session
from models import User
from config import settings 

# Στη δουλειά, αυτό το κλειδί μπαίνει σε αρχείο .env (θα το δούμε στο Μάθημα 6)
SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

password_hash = PasswordHash.recommended()

# Λέει στο FastAPI (και στο Swagger UI!) από ποιο URL παίρνουμε το token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Μετατρέπει τον απλό κωδικό σε hash
def get_password_hash(password: str) -> str:
    return password_hash.hash(password)

# Ελέγχει αν ο κωδικός που πληκτρολόγησε ο χρήστης ταιριάζει με το hash της βάσης
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)

# Δημιουργεί το JWT Token με ημερομηνία λήξης
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# DEPENDENCY-ΦΥΛΑΚΑΣ: Προστατεύει τα endpoints και επιστρέφει τον συνδεδεμένο χρήστη
def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Μη έγκυρο ή ληγμένο token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.InvalidTokenError:
        raise credentials_exception

    user = session.exec(select(User).where(User.username == username)).first()
    if user is None:
        raise credentials_exception
    return user