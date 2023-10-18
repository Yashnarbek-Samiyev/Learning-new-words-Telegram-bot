import sqlalchemy as db
engine = db.create_engine(
    'postgresql+psycopg2://postgres:1223@localhost:5432/memorize')
