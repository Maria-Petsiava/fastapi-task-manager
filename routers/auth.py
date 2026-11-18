from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from database import get_session
from models import User, UserCreate, UserPublic
from security import get_password_hash, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

# 1. ΕΓΓΡΑΦΗ ΧΡΗΣΤΗ (REGISTER)
@router.post("/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, session: Session = Depends(get_session)):
    # Ελέγχουμε αν υπάρχει ήδη το username
    existing_user = session.exec(select(User).where(User.username == user_data.username)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Το όνομα χρήστη χρησιμοποιείται ήδη.")
    
    # Κρυπτογραφούμε τον κωδικό πριν τον αποθηκεύσουμε
    hashed_pw = get_password_hash(user_data.password)
    new_user = User(username=user_data.username, hashed_password=hashed_pw)
    
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

# 2. ΣΥΝΔΕΣΗ (LOGIN) - Επιστρέφει το JWT Token
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    user = session.exec(select(User).where(User.username == form_data.username)).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Λάθος όνομα χρήστη ή κωδικός πρόσβασης",
        )
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}