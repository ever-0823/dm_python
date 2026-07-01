import bcrypt


def hash_password(password: str) -> str:
    """
    把明文转换成hash
    :param password:
    :return:
    """
    return bcrypt.hashpw(password.encode("UTF-8"), bcrypt.gensalt()).decode("UTF-8")


def verify_password(password: str, hashed_password: str) -> bool:
    """
    验证明文密码是否和数据库里的哈希匹配
    :param plain_password:
    :param hashed_password:
    :return:
    """
    return bcrypt.checkpw(password.encode("UTF-8"), hashed_password.encode("UTF-8"))
