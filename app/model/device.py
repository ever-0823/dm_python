import math

# from pygments.lexers.srcinfo import keywords

from app.core.database import db


class Device:

    @staticmethod
    def get_list(page: int = 1, page_size: int = 10, search: str = "", status: str = ""):
        """分页查询列表，支持按设备号或设备名称查找
        #TODO 新增多条件查询，可以灵活地根据是否存在 search 或 status 来决定是否添加条件
        """
        # offset：SQL 从第几条开始取
        offset = (page - 1) * page_size
        # with db.get_cursor() as cursor:
        #     # if search:
        #     keyword = f"%{search}%"
        #     cursor.execute("""SELECT COUNT(*) AS total
        #                       FROM devices
        #                       WHERE device_name LIKE %s
        #                          OR device_id LIKE %s""", (keyword, keyword),
        #                    )
        #     total = cursor.fetchone()["total"]
        #     cursor.execute("""SELECT id, device_id, device_name, model, manufacturer, location, status
        #                       from devices
        #                       where device_name LIKE %s
        #                          OR device_id LIKE %s
        #                       ORDER BY id DESC LIMIT %s
        #                       OFFSET %s""", (keyword, keyword, page_size, offset))
        #     # else:
        #     #     cursor.execute("""SELECT id, device_id, device_name, model, manufacturer, location, status
        #     #                       from devices
        #     #                       ORDER BY id DESC LIMIT %s
        #     #                       OFFSET %s""", (page_size, offset))
        #     items = cursor.fetchall()
        conditions = []  # 查询条件
        params = []  # 查询参数
        if search:
            # append() - 整体添加
            # extend() - 逐个添加
            conditions.append("(device_name LIKE %s OR device_id LIKE %s)")
            keyword = f"%{search}%"
            params.extend([keyword, keyword])
        if status:
            conditions.append("status = %s")
            params.append(status)
        # print(f"conditions:{conditions}")
        # print(f"params:{params}")

        where_clause = ""
        if conditions:
            # " AND ".join(conditions) 是 Python 中的字符串拼接方法
            where_clause = "WHERE " + " AND ".join(conditions)
        print(f"SELECT COUNT(*) AS total FROM devices {where_clause}")

        with db.get_cursor() as cursor:
            cursor.execute(f"""SELECT COUNT(*) AS total FROM devices {where_clause} """, tuple(params), )
            total = cursor.fetchone()["total"]
            cursor.execute(
                f"""SELECT id, device_id, device_name, model, manufacturer, location, status 
                FROM devices {where_clause} ORDER BY id DESC LIMIT %s OFFSET %s""",
                tuple(params + [page_size, offset]), )
            items = cursor.fetchall()

        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": math.ceil(total / page_size),
        }

    """查询全部设备用于导出csv"""

    @staticmethod
    def get_all_for_export():
        with db.get_cursor() as cursor:
            cursor.execute("""SELECT device_id, device_name, model, manufacturer, location, status
                              FROM devices
                              ORDER BY id DESC""")
        return cursor.fetchall()

    """新增设备"""

    @staticmethod
    def create(data: dict):
        with db.get_cursor() as cursor:
            cursor.execute("""INSERT INTO devices (device_id, device_name, model, manufacturer, location, status)
                              VALUES (%s, %s, %s, %s, %s, %s)""",
                           (
                               data['device_id'],
                               data['device_name'],
                               data['model'],
                               data['manufacturer'],
                               data['location'],
                               data['status']
                           ))
            return cursor.lastrowid

    """根据device_id查询"""

    @staticmethod
    def find_by_device_id(device_id: str):
        with db.get_cursor() as cursor:
            cursor.execute("""SELECT id,
                                     device_id,
                                     device_name,
                                     model,
                                     manufacturer,
                                     location,
                                     status,
                                     file_path
                              FROM devices
                              WHERE device_id = %s""", (device_id,))
            return cursor.fetchone()

    """
    按设备编号更新设备信息
    """

    @staticmethod
    def update_by_device_id(device_id: str, data: dict):
        with db.get_cursor() as cursor:
            cursor.execute("""UPDATE devices
                              SET device_name  = %s,
                                  model        = %s,
                                  manufacturer = %s,
                                  location     = %s,
                                  status       = %s
                              WHERE device_id = %s""",
                           (
                               data['device_name'],
                               data['model'],
                               data['manufacturer'],
                               data['location'],
                               data['status'],
                               device_id,
                           ))
            return cursor.rowcount

    @staticmethod
    def delete_by_device_id(device_id: str):
        with db.get_cursor() as cursor:
            cursor.execute("""DELETE
                              FROM devices
                              WHERE device_id = %s""", (device_id,))
            return cursor.rowcount

    @staticmethod
    def delete_by_device_ids(device_ids: list[str]):
        if not device_ids:
            return 0
        placeholders = ", ".join(["%s"] * len(device_ids))
        with db.get_cursor() as cursor:
            cursor.execute(
                f"""DELETE FROM devices
                    WHERE device_id IN ({placeholders})""",
                tuple(device_ids),
            )
            return cursor.rowcount

    """设备状态统计"""

    @staticmethod
    def get_statistics():
        with db.get_cursor() as cursor:
            cursor.execute("""SELECT COUNT(*)                                                AS total,
                                     SUM(CASE WHEN status = 'active' THEN 1 ELSE 0 END)      AS active,
                                     SUM(CASE WHEN status = 'maintenance' THEN 1 ELSE 0 END) AS maintenance,
                                     SUM(CASE WHEN status = 'inactive' THEN 1 ELSE 0 END)    AS inactive,
                                     SUM(CASE WHEN status = 'retired' THEN 1 ELSE 0 END)     AS retired
                              FROM devices
                           """)
            return cursor.fetchone()

    @staticmethod
    def update_file_path(device_id: str, file_path: str):
        with db.get_cursor() as cursor:
            cursor.execute("""UPDATE devices
                              SET file_path = %s
                              WHERE device_id = %s""", (file_path, device_id))
            return cursor.rowcount
