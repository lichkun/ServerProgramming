import json
import mysql.connector
import hashlib
import uuid

class Db:
    def __init__(self, config):
        if isinstance(config, dict):
            if "db" in config:
                self.connection = mysql.connector.connect(**config["db"])
            else:
                self.connection = mysql.connector.connect(**config)
        elif isinstance(config, str):
            try:
                with open(config, 'r') as file:
                    file_config = json.load(file)
                if "db" in file_config:
                    self.connection = mysql.connector.connect(**file_config["db"])
                else:
                    self.connection = mysql.connector.connect(**file_config)
            except FileNotFoundError:
                raise ValueError(f"Configuration file '{config}' not found.")
            except json.JSONDecodeError:
                raise ValueError(f"Configuration file '{config}' contains invalid JSON.")
        else:
            raise TypeError("Config must be a dictionary or a string (file path).")

    def get_connection(self):
        return self.connection


class User:
    def __init__(self, name: str, email: str, password:str, login:str=None ):
        self.name = name
        self.email = email
        self.password = password
        self.login = login if login is not None else email



class UserDao:
    def __init__(self, db: Db):
        self.__db = db

    def create_tables(self):
        connection = self.__db.get_connection()
        sql = """CREATE TABLE users (
        `user_id` CHAR(36) PRIMARY KEY DEFAULT( UUID()),
        `user_name` VARCHAR(128) NOT NULL,
        `user_email` VARCHAR(256) NOT NULL
        ) ENGINE = InnoDB, DEFAULT CHARSET = utf8mb4 COLLATE utf8mb4_unicode_ci
        """
        connection.cursor().execute(sql)

        sql = """CREATE TABLE user_access (
                `ua_id` CHAR(36) PRIMARY KEY DEFAULT( UUID()),
                `user_id` CHAR(36) NOT NULL,
                `ua_login` VARCHAR(256) NOT NULL,
                `ua_hash` VARCHAR(32) NOT NULL,
                `ua_salt` VARCHAR(16) NOT NULL
                ) ENGINE = InnoDB, DEFAULT CHARSET = utf8mb4 COLLATE utf8mb4_unicode_ci
                """
        connection.cursor().execute(sql)
        connection.commit()

    def add_user(self, user: User):
        conn = self.__db.get_connection()
        salt = hashlib.md5(user.password.encode()).hexdigest()[:16]
        password_hash = hashlib.md5(user.password.encode()).hexdigest()

        try:
            sql = "SELECT COUNT(*) FROM user_access WHERE ua_login = %s"
            with conn.cursor() as cursor:
                cursor.execute(sql, (user.login,))
                count = cursor.fetchone()[0]

            if count > 0:
                raise ValueError(f"Login '{user.login}' is already in use.")

            user_id = str(uuid.uuid4())

            sql = "INSERT INTO users (`user_id`, `user_name`, `user_email`) VALUES (%s, %s, %s)"
            with conn.cursor() as cursor:
                cursor.execute(sql, (user_id, user.name, user.email))

            sql = "INSERT INTO user_access (`user_id`, `ua_login`, `ua_hash`, `ua_salt`) VALUES (%s, %s, %s, %s)"
            with conn.cursor() as cursor:
                cursor.execute(sql, (user_id, user.login, password_hash, salt))

            conn.commit()

        except mysql.connector.Error as err:
            conn.rollback() 
            raise err

def main():
    try:
        db = Db('db_config.json')
        print("DB connected")
        sql = "SHOW DATABASES"
        with db.get_connection().cursor() as cursor:
            cursor.execute(sql)
            print(cursor.column_names)
            for row in cursor:
                print(row)

        # db = Db({
        #     'host': 'localhost',
        #     'port': 3308,
        #     'user': 'py213_user',
        #     'password': 'py213_pass',
        #     'database': 'py_knp_213',
        #     'charset': 'utf8mb4',
        #     'collation': 'utf8mb4_unicode_ci',
        # })
        # print("DB connected")

    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
    except ValueError as ve:
        print(f"Value error: {ve}")
    except TypeError as te:
        print(f"Type error: {te}")

    userDao = UserDao(db)
    try:
        pass
    except mysql.connector.Error as err:
        print(err)
        return

    try:
        userDao.add_user(User('The User2', 'user2@i.ua', '12334'))
    except mysql.connector.Error as err:
        print(err)
        return
    else:
        print("I --- userDao. create_tables() OK ---")

if __name__ == "__main__": main()