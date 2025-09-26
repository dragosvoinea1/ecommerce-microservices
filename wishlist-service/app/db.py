import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Preluăm URL-ul bazei de date din variabilele de mediu
DATABASE_URL = os.environ.get("DATABASE_URL")

# Creăm "motorul" SQLAlchemy
engine = create_engine(DATABASE_URL)

# Creăm o sesiune de conexiune
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# O clasă de bază pentru modelele noastre de date
Base = declarative_base()