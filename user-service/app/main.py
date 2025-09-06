from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import models, db, security
from jose import JWTError, jwt
import os
import secrets
from datetime import datetime, timedelta

# Creează tabelul 'users' la pornire
models.Base.metadata.create_all(bind=db.engine)

# Inițializează aplicația principală FĂRĂ root_path
app = FastAPI(title="Users Service")

# Router pentru rutele de autentificare (FĂRĂ prefix)
auth_router = APIRouter(tags=["Authentication"])

# Router pentru rutele de utilizator (CU prefix /users)
users_router = APIRouter(prefix="/users", tags=["Users"])

# Definim schema de securitate. tokenUrl este calea relativă la rădăcina aplicației.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_db():
    database = db.SessionLocal()
    try:
        yield database
    finally:
        database.close()

async def get_current_user(token: str = Depends(oauth2_scheme), database: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = database.query(models.DBUser).filter(models.DBUser.email == email).first()
    if user is None:
        raise credentials_exception
    return user

# --- Endpoint-urile sunt atașate la routerele corecte ---

@auth_router.post("/register", response_model=models.User, status_code=status.HTTP_201_CREATED)
def register_user(user_data: models.UserCreate, database: Session = Depends(get_db)):
    if database.query(models.DBUser).filter(models.DBUser.email == user_data.email).first():
        raise HTTPException(status_code=400, detail="Acest email este deja înregistrat.")
    if database.query(models.DBUser).filter(models.DBUser.phone_number == user_data.phone_number).first():
        raise HTTPException(status_code=400, detail="Acest număr de telefon este deja înregistrat.")
    
    hashed_password = security.get_password_hash(user_data.password)
    confirmation_token = secrets.token_urlsafe(32)
    token_expiration = datetime.utcnow() + timedelta(hours=1)
    
    new_user = models.DBUser(
        email=user_data.email, hashed_password=hashed_password,
        full_name=user_data.full_name, phone_number=user_data.phone_number,
        address=user_data.address, city=user_data.city, country=user_data.country,
        is_active=False, confirmation_token=confirmation_token, token_expiration=token_expiration
    )
    
    database.add(new_user)
    database.commit()
    database.refresh(new_user)

    print("--- EMAIL DE CONFIRMARE ---")
    print(f"Pentru: {new_user.email}")
    print(f"Click pe link: http://localhost:5173/confirm/{confirmation_token}")
    print("---------------------------")

    return new_user

@auth_router.get("/confirm/{token}", response_model=models.User)
def confirm_account(token: str, db: Session = Depends(get_db)):
    user = db.query(models.DBUser).filter(models.DBUser.confirmation_token == token).first()
    if not user:
        raise HTTPException(status_code=404, detail="Token invalid.")
    if user.token_expiration < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Token expirat.")
    
    user.is_active = True
    user.confirmation_token = None
    user.token_expiration = None
    db.commit()
    db.refresh(user)
    return user

@auth_router.post("/login")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), database: Session = Depends(get_db)):
    user = database.query(models.DBUser).filter(models.DBUser.email == form_data.username).first()
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Contul nu este activat. Verifică-ți email-ul."
        )
    
    token_data = {"sub": user.email, "role": user.role}
    access_token = security.create_access_token(data=token_data)
    return {"access_token": access_token, "token_type": "bearer"}

@users_router.get("/me", response_model=models.User)
async def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user

# Includem ambele routere în aplicația principală
app.include_router(auth_router)
app.include_router(users_router)