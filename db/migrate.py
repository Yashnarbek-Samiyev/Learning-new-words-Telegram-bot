from table import Base
from engine import engine
Base.metadata.create_all(engine)
