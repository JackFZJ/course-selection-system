import functools
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt

# 装饰器
# def login_stu(func):
#     @functools.wraps(func)
#     def inner(*args, **kwargs):
#         stu_id = session.get('student_id')
#         if stu_id:
#             return func(*args, **kwargs)
#         else:
#             return {
#                 'code': 1,
#                 'msg': '学生未登录'
#             }

#     return inner


# def login_admin(func):
#     @functools.wraps(func)
#     def inner(*args, **kwargs):
#         admin_name = session.get('admin_name')
#         if admin_name:
#             return func(*args, **kwargs)
#         else:
#             return {
#                 'code': 1,
#                 'msg': '管理员未登录'
#             }

#     return inner

def admin_required():
 def wrapper(fn):
     @functools.wraps(fn)
     def decorator(*args, **kwargs):
         verify_jwt_in_request()
         claims = get_jwt()
         if claims.get("is_admin"):
             return fn(*args, **kwargs)
         else:
             return jsonify(code=1,msg="需要管理员登录"), 403
     return decorator
 return wrapper

def student_required():
 def wrapper(fn):
     @functools.wraps(fn)
     def decorator(*args, **kwargs):
         verify_jwt_in_request()
         claims = get_jwt()
         if claims.get("is_student"):
             return fn(*args, **kwargs)
         else:
             return jsonify(code=1,msg="需要学生登录"), 403
     return decorator
 return wrapper