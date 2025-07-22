import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Preluam URL-ul bazei de date din variabilele de mediu setate in docker-compose.yml
DATABASE_URL = os.environ.get("DATABASE_URL")

# Cream "motorul" SQLAlchemy
engine = create_engine(DATABASE_URL)

# Cream o sesiune de conexiune
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# O clasa de baza pentru modelele noastre de date
Base = declarative_base()
