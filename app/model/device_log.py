from ..core.database import db

"""
--device_id：哪台设备
--action：做了什么，比如 create、update、delete
--operator：是谁操作的
--details：补充说明
--created_at：操作时间

"""

"""写入一条设备操作日志"""

class DeviceLog:
    @staticmethod
    def create(device_id: str, action: str, operation: str, details: str = ""):
        # print(f"device_log->operation:{operation}")
        print("INSERT INTO device_logs (device_id, action, operation, details) VALUES (%s, %s, %s, %s)",(device_id, action, operation, details))
        with db.get_cursor() as cursor:
            cursor.execute(
                """INSERT INTO device_logs (device_id, action, operator, details)
                   VALUES (%s, %s, %s, %s)""",
                (device_id, action, operation, details),
            )
        return cursor.lastrowid

    """ 查询某台设备的操作日志，按最新时间倒序。"""

    @staticmethod
    def get_device_id(device_id: str):
        with db.get_cursor() as cursor:
            cursor.execute(
                """SELECT id, device_id, action, operator, details
                   FROM device_logs
                   WHERE device_id = %s
                   ORDER BY id DESC""",
                (device_id,),
            )
            return cursor.fetchall()
