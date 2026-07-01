import bcrypt


def hash_password(password: str) -> str:
    """
    把明文转化成哈希
    password.encode("utf-8") 将密码字符串转换为字节序列（bcrypt 处理的是 bytes）
    bcrypt.gensalt() 生成一个随机盐值（Salt），用于防彩虹表攻击
    bcrypt.hashpw() 使用 bcrypt 算法对密码+盐值进行哈希计算
    .decode("utf-8")    将哈希结果的字节转换回字符串，便于数据库存储
    """
    return bcrypt.hashpw(password.encode("UTF-8"), bcrypt.gensalt()).decode("UTF-8")
