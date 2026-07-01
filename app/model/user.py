from app.core.database import db


class User:
    @staticmethod
    def get_all():
        with db.get_cursor() as cursor:
            cursor.execute('SELECT * FROM users ORDER BY id DESC')
            return cursor.fetchall()

    @staticmethod
    def find_by_username(username):
        with db.get_cursor() as cursor:
            cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
            return cursor.fetchone()

    """新增用户"""
    @staticmethod
    def create(username:str, password_hash:str, role:str="user"):
        with db.get_cursor() as cursor:
            cursor.execute('INSERT INTO users (username, password_hash,role) VALUES (%s, %s,%s)',
                           (username, password_hash,role))
            #用于获取最后一次插入操作生成的自动递增 ID
            return cursor.lastrowid 