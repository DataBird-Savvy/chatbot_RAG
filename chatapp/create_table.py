from chatapp.db.db import engine
from chatapp.db.models import Base

Base.metadata.create_all(bind=engine)