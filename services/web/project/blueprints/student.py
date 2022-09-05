# --*--coding: utf-8 --*--
from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash
from project.schemas import CourseSchema
from project.models import StuToCourse, StuModel, CourseModel
from project.decorators import student_required
from project.extensions import rpc
from flask_jwt_extended import current_user,get_jwt
# 注册蓝图
bp = Blueprint("student", __name__, url_prefix='/student')

course_schema = CourseSchema()


@bp.route("/login/", methods=['POST', ])
def student_login():
    data = request.form
    res=rpc.services_student.student_login.call_async(data)
    return res.result()


@bp.route("/logout/", methods=['DELETE', ])
@student_required()
def student_logout():
    jti = get_jwt()["jti"]
    res=rpc.services_student.student_logout.call_async(jti)
    return res.result()

@bp.route("/course/", methods=['GET', ])
@student_required()
def get_course():
    student_id = current_user.student_id
    search = request.args.get('search')
    res=rpc.services_student.student_get_courses.call_async(student_id,search)
    return res.result()


@bp.route("/selected_course/", methods=['GET', ])
@student_required()
def get_selected_course():
    student_id = current_user.student_id
    res=rpc.services_student.student_get_selected_courses.call_async(student_id)
    return res.result()
    # return res.result()


@bp.route("/select_course/<course_id>", methods=['GET', ])
@student_required()
def select_course(course_id):
    student_id = current_user.student_id
    res=rpc.services_student.student_select_course.call_async(student_id,course_id)
    return res.result()


@bp.route("/drop_course/<course_id>", methods=['GET', ])
@student_required()
def drop_course(course_id):
    student_id = current_user.student_id
    res=rpc.services_student.student_drop_course.call_async(course_id,student_id)
    return res.result()
