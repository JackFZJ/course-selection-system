# --*--coding: utf-8 --*--
from flask import Blueprint, request, session
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash
from project.schemas import CourseSchema
from project.models import StuToCourse, StuModel, CourseModel
from project.decorators import login_stu
from project.extensions import db

# 注册蓝图
bp = Blueprint("student", __name__, url_prefix='/student')

course_schema = CourseSchema()


@bp.route("/login/", methods=['POST', ])
def student_login():
    data = request.form
    student = StuModel.query.filter_by(student_id=data.get('id')).first()
    if student and check_password_hash(student.password, data.get('password')):
        session["student_id"] = student.student_id
        return {
            'code': 0,
            'msg': '登录成功'
        },200
    else:
        return {
            'code': 1,
            'msg': '学号或密码错误'
        },401


@bp.route("/logout/", methods=['GET', ])
def student_logout():
    if session.get('student_id'):
        session.pop('student_id')
        return {
            'code': 0,
            'msg': '注销成功'
        }
    else:
        return {
            'code': 1,
            'msg': '注销失败'
        }


@bp.route("/course/", methods=['GET', ])
@login_stu
def get_course():
    student_id = session.get('student_id')
    stu_courses = StuToCourse.query.filter_by(student_id=student_id).order_by("course_id").all()
    search = request.args.get('search')
    if not search:
        courses = CourseModel.query.order_by("course_id").all()
    else:
        courses = CourseModel.query.filter(
            db.or_(CourseModel.name.contains(search), CourseModel.desc.contains(search))).order_by("course_id").all()
    for stu_course in stu_courses:
        for course in courses:
            if course.course_id == stu_course.course_id:
                courses.remove(course)
    if courses:
        return {
            'code': 0,
            'msg': '查询可选课程成功',
            'data': course_schema.dump(courses, many=True)
        }
    else:
        return {
            'code': 0,
            'msg': '没有可选课程'
        }


@bp.route("/selected_course/", methods=['GET', ])
@login_stu
def get_selected_course():
    student_id = session.get('student_id')
    # student = StuModel.query.filter_by(student_id=student_id).first()
    # courses = student.courses
    # 子查询
    subq = db.session.query(StuToCourse.course_id.label('cid')).filter(StuToCourse.student_id == student_id).subquery()
    courses = CourseModel.query.filter(CourseModel.course_id == subq.c.cid).order_by("course_id").all()
    if courses:
        return {
            'code': 0,
            'msg': '查询已选课程成功',
            'data': course_schema.dump(courses, many=True)
        }
    else:
        return {
            'code': 0,
            'msg': '没有已选课程'
        }


@bp.route("/select_course/<course_id>", methods=['GET', ])
@login_stu
def select_course(course_id):
    student_id = session.get('student_id')
    course = CourseModel.query.filter_by(course_id=course_id).first()
    if not course:
        return {
            'code': 1,
            'msg': "未找到课程"
        }
    stu_course = StuToCourse().query.filter_by(student_id=student_id,course_id=course_id).first()
    if stu_course:
        return {
            'code': 1,
            'msg': '请勿重复选课'
        }
    if course.volume == 0:
        return {
            'code': 1,
            'msg': '课程容量已满'
        }
    course.volume -= 1  # 被选后课容量减一

    stu_course = StuToCourse()
    stu_course.course_id = course_id
    stu_course.student_id = student_id
    stu_course.save_to_db()
    return {
        'code': 0,
        'msg': '选课成功'
    }



@bp.route("/drop_course/<course_id>", methods=['GET', ])
@login_stu
def drop_course(course_id):
    student_id = session.get('student_id')
    stu_course = StuToCourse.query.filter_by(course_id=course_id, student_id=student_id).first()
    if not stu_course:
        return {
            'code': 1,
            'msg': "未找到课程"
        }
    course = CourseModel.query.filter_by(course_id=course_id).first()
    course.volume += 1
    stu_course.delete_from_db()
    return {
        'code': 0,
        'msg': '退课成功'
    }
