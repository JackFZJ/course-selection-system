import functools
from flask import session, redirect, url_for


# 装饰器
def login_stu(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        stu_id = session.get('student_id')
        if stu_id:
            return func(*args, **kwargs)
        else:
            return {
                'code': 1,
                'msg': '学生未登录'
            }

    return inner


def login_admin(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        admin_name = session.get('admin_name')
        if admin_name:
            return func(*args, **kwargs)
        else:
            return {
                'code': 1,
                'msg': '管理员未登录'
            }

    return inner
