"""
统一成功响应格式
data:主要返回数据
message:成功提示信息
extra:额外字段,比如 current_user,operator
"""


def success_response(data=None, message: str = "ok", **extra):
    response = {
        "success": True,
        "message": message,
        "data": data,
    }
    response.update(extra)
    return response
