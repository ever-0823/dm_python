from email import message

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

import pymysql


class AppException(Exception):
    """
    自定义业务异常
    code:HTTP状态码
    message:返回给前端的错误信息
    """

    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message


def register_exception_handlers(app: FastAPI):
    """
    给 FastAPI 注册全局异常处理器
    :param app:
    :return:
    """

    @app.exception_handler(AppException)
    async def handel_app_exception_handler(request: Request, exc: AppException):
        return JSONResponse(status_code=exc.code, content={
            "success": False,
            "message": exc.message,
        })

    @app.exception_handler(RequestValidationError)
    async def handle_validation_exception(request: Request, exc: RequestValidationError):
        return JSONResponse(status_code=422,
                            content={
                                "success": False,
                                "message": "参数校验失败",
                                "errors": exc.errors(),
                            })

    @app.exception_handler(pymysql.err.IntegrityError)
    async def handle_integrity_error(request: Request, exc: pymysql.err.IntegrityError):
        """
        代码层提前查重：给正常场景更友好的提示
        数据库唯一索引：兜底保证数据不会重复
        全局异常处理：把数据库异常转成前端能看懂的 JSON
        """
        error_code = exc.args[0] if exc.args else None

        if error_code == 1062:
            message = "数据已存在,不能重复创建"
        else:
            message = "数据库完整性约束错误"
        return JSONResponse(status_code=400, content={
            "success": False,
            "message": message,
        })
