from contextlib import contextmanager

from app.core.config import settings
import pymysql


class Database:
    """
    数据库连接获取方法，用于创建并返回一个 PyMySQL 数据库连接对象
    """

    def get_connection(self):

        return pymysql.connect(
            host=settings.DB_HOST,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            db=settings.DB_NAME,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,  # 返回字典格式
            autocommit=False,  # 关闭自动提交
        )

    """装饰器，将函数转换为上下文管理器"""

    @contextmanager
    def get_cursor(self):
        conn = self.get_connection()
        cursor = conn.cursor()  # 创建一个游标（Cursor）对象
        try:
            yield cursor  # 将游标返回给调用者（暂停执行）
            conn.commit()
        except Exception:
            conn.rollback()  # 如果发生异常，回滚事务
            raise  # 重新抛出异常
        finally:
            cursor.close()
            conn.close()


db = Database()
