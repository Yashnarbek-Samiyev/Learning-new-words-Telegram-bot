from db.table import UsersTable
from db.engine import engine
from sqlalchemy.orm import sessionmaker


def register(telegram_id, first_name, last_name):
    """
    Register a user in the database
    """
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        user = UsersTable(telegram_id=telegram_id,
                          first_name=first_name, last_name=last_name)
        session.add(user)
        session.commit()

    except Exception as e:
        print(e)


def get_user_data(telegram_id):
    Session = sessionmaker(bind=engine)
    session = Session()

    result = session.query(UsersTable).filter(
        UsersTable.telegram_id == telegram_id).first()
    return result if result else None
