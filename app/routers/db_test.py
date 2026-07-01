"""
数据库连通性测试
"""
from fastapi import APIRouter

from app.core.database import db

router = APIRouter()


@router.get("/db/ping")
def db_ping():
    with db.get_cursor() as cursor:
        cursor.execute('SELECT 1 AS OK')
        result = cursor.fetchone()  # 从查询结果集中获取下一行数据

        return {
            "success": True,
            "message": "database connected",
            "data": result,
        }
