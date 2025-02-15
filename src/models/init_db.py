from .base import Base, engine
from .models import Client, Cleaner, Job, Roster, Invoice, Payment

def init_db():
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_db()
