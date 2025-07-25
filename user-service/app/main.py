from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import models, db, security
from jose import JWTError, jwt
import os

# Creeaza tabelul 'users' la pornire
models.Base.metadata.create_all(bind=db.engine)

ROOT_PATH = os.environ.get("ROOT_PATH", "")
app = FastAPI(title="Users Service", root_path=ROOT_PATH)

# --- NOU: Schema de securitate pentru a citi token-ul din header ---
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# Functie pentru a obtine sesiunea de DB
def get_db():
    database = db.SessionLocal()
    try:
        yield database
    finally:
        database.close()


# --- NOU: Functie pentru a obtine utilizatorul curent din token ---
async def get_current_user(token: str = Depends(oauth2_scheme),
                           database: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token,
                             security.SECRET_KEY,
                             algorithms=[security.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = database.query(
        models.DBUser).filter(models.DBUser.email == email).first()
    if user is None:
        raise credentials_exception
    return user


@app.post("/register",
          response_model=models.User,
          status_code=status.HTTP_201_CREATED)
def register_user(user_data: models.UserCreate,
                  database: Session = Depends(get_db)):
    """Inregistreaza un utilizator nou."""
    db_user = database.query(
        models.DBUser).filter(models.DBUser.email == user_data.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = security.get_password_hash(user_data.password)
    new_user = models.DBUser(email=user_data.email,
                             hashed_password=hashed_password)

    database.add(new_user)
    database.commit()
    database.refresh(new_user)
    return new_user


@app.post("/login")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                           database: Session = Depends(get_db)):
    """Autentifica un utilizator si returneaza un token."""
    user = database.query(models.DBUser).filter(
        models.DBUser.email == form_data.username).first()
    if not user or not security.verify_password(form_data.password,
                                                user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = security.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


# --- NOU: Endpoint-ul protejat ---
@app.get("/me", response_model=models.User)
async def read_users_me(current_user: models.User = Depends(get_current_user)):
    """
    Returneaza datele utilizatorului autentificat.
    Necesita un token valid.
    """
    return current_user
