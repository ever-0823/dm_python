from fastapi import Depends
from app.core.auth import get_current_user

def current_user(user=Depends(get_current_user)):
    """
    把当前登录用户注入到接口函数里
    :param user:
    :return:
    """
    return user
