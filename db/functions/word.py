from sqlalchemy.orm import sessionmaker
from db.engine import engine
from db.table import WordsTable, UsersWordsTable, StatusEnum
from sqlalchemy.sql.expression import func, select


def get_user_word(user_id):
    # Return new word for user with user_id
    # If there is no new word for user, return None

    Session = sessionmaker(bind=engine)
    session = Session()
    subquery = session.query(UsersWordsTable.word_id).filter(
        UsersWordsTable.user_id == user_id).subquery()
    result = session.query(WordsTable).filter(
        WordsTable.id.not_in(subquery)).order_by(func.random()).first()
    return result if result else None


def get_word_by_id(word_id):

    Session = sessionmaker(bind=engine)
    session = Session()

    result = session.query(WordsTable).filter(
        WordsTable.id == word_id).first()
    return result if result else None


def get_user_review_word(user_id):
    # Return new word for user with user_id
    # If there is no new word for user, return None

    Session = sessionmaker(bind=engine)
    session = Session()
    subquery = session.query(UsersWordsTable.word_id).filter(
        UsersWordsTable.user_id == user_id, UsersWordsTable.status == StatusEnum.learn).subquery()
    result = session.query(WordsTable).filter(
        WordsTable.id.in_(subquery)).order_by(func.random()).first()
    return result if result else None


def users_words_create(user_id, word_id, status):
    """
    Register a user in the database
    """

    Session = sessionmaker(bind=engine)
    session = Session()
    userswords = UsersWordsTable(user_id=user_id,
                                 word_id=word_id, status=StatusEnum(int(status)))
    session.add(userswords)
    session.commit()


def users_words_update(user_id, word_id, status):
    """
    Register a user in the database
    """

    Session = sessionmaker(bind=engine)
    session = Session()

    session.query(UsersWordsTable).filter(
        UsersWordsTable.user_id == user_id, UsersWordsTable.word_id == word_id).update({'status': StatusEnum(int(status))})
    session.commit()


def word_create(word, word_translation, photo=None, audio=None):
    """
    Register a user in the database
    """

    Session = sessionmaker(bind=engine)
    session = Session()
    word = WordsTable(word=word,
                      word_translation=word_translation, photo=photo, audio=audio)
    session.add(word)
    session.commit()
