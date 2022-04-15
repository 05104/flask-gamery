from models.game import Game
from models.user import User

SQL_DELETE_GAME = 'delete FROM games WHERE id = %s'
SQL_GAME_BY_ID = 'SELECT id, name, category, console, created_at FROM games WHERE id = %s'
SQL_USER_BY_ID = 'SELECT * FROM users WHERE id = %s'
SQL_USER_BY_NAME = 'SELECT * FROM users WHERE username = %s'
SQL_UPDATE_GAME = 'UPDATE games SET name=%s, category=%s, console=%s WHERE id = %s'
SQL_SEARCH_GAMES = 'SELECT id, name, category, console, created_at FROM games'
SQL_CREATE_GAME = 'INSERT into games (name, category, console) values (%s, %s, %s) RETURNING id'

class GameDao:
    def __init__(self, db):
        self.__db = db

    def save(self, game):
        cursor = self.__db.cursor()

        print(game.id)
        if (game.id):
            cursor.execute(SQL_UPDATE_GAME, (game.name, game.category, game.console, game.id))
        else:
            cursor.execute(SQL_CREATE_GAME, (game.name, game.category, game.console))
            game.id = cursor.fetchone()[0]
            
        self.__db.commit()
        
        return game

    def list(self):
        cursor = self.__db.cursor()
        cursor.execute(SQL_SEARCH_GAMES)
        games = translate_games(cursor.fetchall())
        return games

    def find_by_id(self, id):
        cursor = self.__db.cursor()
        cursor.execute(SQL_GAME_BY_ID, (id,))
        tuple = cursor.fetchone()
        return Game(tuple[1], tuple[2], tuple[3], tuple[0], tuple[4])

    def delete(self, id):
        self.__db.cursor().execute(SQL_DELETE_GAME, (id, ))
        self.__db.commit()


class UserDao:
    def __init__(self, db):
        self.__db = db

    def find_by_id(self, id):
        cursor = self.__db.cursor()
        cursor.execute(SQL_USER_BY_ID, (id,))
        datas = cursor.fetchone()
        user = translate_users(datas) if datas else None
        return user

    def find_by_name(self, username):
        cursor = self.__db.cursor()
        cursor.execute(SQL_USER_BY_NAME, (username,))
        datas = cursor.fetchone()
        user = translate_users(datas) if datas else None
        return user


def translate_games(games):
    def create_games_with_tuple(tuple):
        return Game(tuple[1], tuple[2], tuple[3], tuple[0], tuple[4])
    return list(map(create_games_with_tuple, games))


def translate_users(tuple):
    return User(tuple[0], tuple[1], tuple[2], tuple[3])
