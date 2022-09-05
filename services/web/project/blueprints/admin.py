# --*--coding: utf-8 --*--
from flask import Blueprint, request
from marshmallow import ValidationError
from project.models import AdminModel, StuModel, CourseModel, StuToCourse,TokenBlocklist
from project.schemas import AdminSchema, StudentSchema, CourseSchema
from project.forms import editcourseForm
from project.decorators import admin_required
from project.extensions import rpc
from flask_jwt_extended import get_jwt


# 注册蓝图
bp = Blueprint("admin", __name__, url_prefix='/admin')
admin_schema = AdminSchema()
student_schema = StudentSchema()
course_schema = CourseSchema()


@bp.route("/login/", methods=['POST', ])
def admin_login():
    data = request.form
    res=rpc.services_admin.admin_login.call_async(data)
    return res.result()


@bp.route("/logout/", methods=["DELETE"])
@admin_required()
def admin_logout():
    jti = get_jwt()["jti"]
    res=rpc.services_admin.admin_logout.call_async(jti)
    return res.result()
    

# @bp.route("/logout/", methods=['GET', ])
# def admin_logout():
#     res=rpc.services_admin.admin_logout.call_async(session.get('admin_name'))
#     if res.result().get('code')==0:
#         session.pop('admin_name')
#     return res.result()

@bp.route("/student/", methods=['POST', ])
@admin_required()
def add_student():
    data = request.form
    res=rpc.services_admin.admin_add_student.call_async(data)
    return res.result()

@bp.route("/student/<student_id>", methods=['DELETE', ])
@admin_required()
def delete_student(student_id):
    res=rpc.services_admin.admin_delete_student.call_async(student_id)
    return res.result()

@bp.route("/student/<student_id>", methods=['PUT', ])
@admin_required()
def edit_student(student_id):
    data = dict(request.form)
    res=rpc.services_admin.admin_edit_student.call_async(student_id,data)
    return res.result()


@bp.route("/student/", defaults={'student_id': None}, methods=['GET', ])
@bp.route("/student/<student_id>", methods=['GET', ])
@admin_required()
def get_student(student_id):
    search = request.args.get('search')
    res=rpc.services_admin.admin_get_student.call_async(student_id,search)
    # if res.result().get('msg')=='查询学生成功':
    #     res.result()['data']=student_schema.dump(res.get('data'),many=True)
    return res.result()


@bp.route("/course/", methods=['POST', ])
@admin_required()
def add_course():
    data = request.form
    res=rpc.services_admin.admin_add_course.call_async(data)
    return res.result()

@bp.route("/course/<course_id>", methods=['DELETE', ])
@admin_required()
def delete_course(course_id):
    res=rpc.services_admin.admin_delete_course.call_async(course_id)
    return res.result()


@bp.route("/course/<course_id>", methods=['PUT', ])
@admin_required()
def edit_course(course_id):
    data = request.form
    form = editcourseForm(data)
    validate_flag=False
    if form.validate():
        validate_flag=True
    else:
        return {
            'code': 1,
            'msg': form.errors
        }
    res=rpc.services_admin.admin_edit_course.call_async(course_id,data,validate_flag)
    return res.result()


@bp.route("/course/", defaults={'course_id': None}, methods=['GET', ])
@bp.route("/course/<course_id>", methods=['GET', ])
@admin_required()
def get_course(course_id):
    search = request.args.get('search')
    res=rpc.services_admin.admin_get_course.call_async(course_id,search)
    return res.result()
    # return res.result()
