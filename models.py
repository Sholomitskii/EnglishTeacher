import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Word(Base):
    __tablename__ = 'word'

    id = sq.Column(sq.Integer, primary_key = True)
    russian_word = sq.Column(sq.String(length=40), unique=True)
    target_word = sq.Column(sq.String(length=40), unique=True)

    def __str__(self):
        return f'Words {self.id}: ({self.russian_word}, {self.target_word})'

class User(Base):
    __tablename__ = 'user'

    id = sq.Column(sq.Integer, primary_key = True)
    usid = sq.Column(sq.BIGINT, unique=True)

    def __str__(self):
        return f'Users {self.id}: ({self.usid})'
    
class User_word(Base):
    __tablename__ = 'user_word'

    id = sq.Column(sq.Integer, primary_key = True)
    id_word = sq.Column(sq.Integer, sq.ForeignKey('word.id'))
    id_user = sq.Column(sq.Integer, sq.ForeignKey('user.id'))

    word = relationship(Word, backref="user_words")
    user = relationship(User, backref="user_words")

    def __str__(self):
        return f'User words {self.id}: ({self.id_word}, {self.id_user})'

class Other_words(Base):
    __tablename__ = 'other words'

    id = sq.Column(sq.Integer, primary_key = True)
    other_word = sq.Column(sq.String(length=40), unique=True)

    def __str__(self):
        return f'Other words {self.id}: ({self.other_word})'

class Command:
    ADD_WORD = 'Добавить слово (+)'
    DELETE_WORD = 'Удалить слово (-)'
    NEXT_WORD = 'Дальше ->'

def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)




