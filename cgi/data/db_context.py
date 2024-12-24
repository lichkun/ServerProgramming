from data.db import Db
from data.user_dao import UserDao


class DbContext:
    def __init__(self):
        self.__db = Db()
        self.user_dao = UserDao(self.__db)

    def test_connection(self):
        return self.__db.get_connection() is not None
    