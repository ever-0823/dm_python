import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """
    os.getenv(key, default)
    APP_NAME = os.getenv("APP_NAME", "Practice Server")
    属性名 环境变量名 默认值
    """
    APP_NAME = os.getenv("APP_NAME", "Practice Server")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", "3306"))
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "1234")
    DB_NAME = os.getenv("DB_NAME", "practice_db")

    #os.path.join()路径拼接函数
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    #UPLOAD_FOLDER 就是“文件最终保存到哪里
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

# 创建一个 Settings 实例，方便在项目其他地方导入使用
settings = Settings()
