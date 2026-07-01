from fastapi import APIRouter

# TODO类创建一个路由路由器实例
router = APIRouter()


# 健康检查接口
@router.get("/health")
def health():
    return {"status": "ok"}
