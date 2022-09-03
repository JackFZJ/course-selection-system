# --*--coding: utf-8 --*--
from flask import Blueprint, request, session
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash
from project.schemas import CourseSchema
from project.models import StuToCourse, StuModel, CourseModel
from project.decorators import login_stu
from project.extensions import db,rpc

# 注册蓝图
bp = Blueprint("student", __name__, url_prefix='/student')

course_schema = CourseSchema()


@bp.route("/login/", methods=['POST', ])
def student_login():
    data = request.form
    res=rpc.services_student.student_login.call_async(data)
    if res.result().get('code')==0:
        session["student_id"] = data.get('id')
    return res.result()


@bp.route("/logout/", methods=['GET', ])
def student_logout():
    res=rpc.services_student.student_logout.call_async(session.get('student_id'))
    if res.result().get('code')==0:
        session.pop('student_id')
    return res.result()
    # return res.result()


@bp.route("/course/", methods=['GET', ])
@login_stu
def get_course():
    student_id = session.get('student_id')
    search = request.args.get('search')
    res=rpc.services_student.student_get_courses.call_async(student_id,search)
    return res.result()


@bp.route("/selected_course/", methods=['GET', ])
@login_stu
def get_selected_course():
    student_id = session.get('student_id')
    res=rpc.services_student.student_get_selected_courses.call_async(student_id)
    return res.result()
    # return res.result()


@bp.route("/select_course/<course_id>", methods=['GET', ])
@login_stu
def select_course(course_id):
    student_id = session.get('student_id')
    res=rpc.services_student.student_select_course.call_async(student_id,course_id)
    return res.result()


@bp.route("/drop_course/<course_id>", methods=['GET', ])
@login_stu
def drop_course(course_id):
    student_id = session.get('student_id')
    res=rpc.services_student.student_drop_course.call_async(course_id,student_id)
    return res.result()
