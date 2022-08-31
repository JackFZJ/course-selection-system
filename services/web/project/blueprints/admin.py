# --*--coding: utf-8 --*--
from flask import Blueprint, request, session,jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from marshmallow import ValidationError
from project.models import AdminModel, StuModel, CourseModel, StuToCourse
from project.schemas import AdminSchema, StudentSchema, CourseSchema
from project.forms import editstuForm, editcourseForm
from project.decorators import login_admin
from project.extensions import db

# 注册蓝图
bp = Blueprint("admin", __name__, url_prefix='/admin')
admin_schema = AdminSchema()
student_schema = StudentSchema()
course_schema = CourseSchema()


@bp.route("/login/", methods=['POST', ])
def admin_login():
    data = request.form
    admin = AdminModel.query.filter_by(name=data.get('name')).first()
    if admin and check_password_hash(admin.password, data.get('password')):
        session["admin_name"] = admin.name
        return {
            'code': 0,
            'msg': '登录成功'
        },200
    else:
        return {
            'code': 1,
            'msg': '用户名或密码错误'
        },401


@bp.route("/logout/", methods=['GET', ])
def admin_logout():
    if session.get('admin_name'):
        session.pop('admin_name')
        return {
            'code': 0,
            'msg': '管理员注销成功'
        }
    else:
        return {
            'code': 1,
            'msg': '管理员注销失败'
        }


@bp.route("/student/", methods=['POST', ])
@login_admin
def add_student():
    data = request.form
    try:
        student = student_schema.load(data)
        student.save_to_db()
        return {
            'code': 0,
            'msg': '添加学生成功'
        }
    except ValidationError as e:
        return {
            'code': 1,
            'msg': e.messages
        }


@bp.route("/student/<student_id>", methods=['DELETE', ])
@login_admin
def delete_student(student_id):
    student = StuModel.query.filter_by(student_id=student_id).first()
    if student:
        # 删除该学生的课程
        stu_course = StuToCourse.query.filter_by(student_id=student_id).all()
        if stu_course:
            for i in stu_course:
                i.delete_from_db()
        student.delete_from_db()
        return {
            'code': 0,
            'msg': '删除学生成功'
        }
    else:
        return {
            'code': 1,
            'msg': '删除学生失败'
        }


@bp.route("/student/<student_id>", methods=['PUT', ])
@login_admin
def edit_student(student_id):
    student = StuModel.query.filter_by(student_id=student_id).first()
    if student:
        data = request.form
        form = editstuForm(data)
        if form.validate():
            for column in student.__table__.columns:
                if column.name not in ('student_id' , 'updated', 'id' , 'created'): setattr(student, column.name, data.get(column.name))
            student.password = generate_password_hash(data.get('password'))
            student.save_to_db()
            return {
                'code': 0,
                'msg': '修改学生成功'
            }
        else:
            return {
                'code': 1,
                'msg': form.errors
            }
    else:
        return {
            'code': 1,
            'msg': '修改学生失败'
        }


@bp.route("/student/", defaults={'student_id': None}, methods=['GET', ])
@bp.route("/student/<student_id>", methods=['GET', ])
@login_admin
def get_student(student_id):
    if not student_id:
        search = request.args.get('search')
        if not search:
            students = StuModel.query.order_by("student_id").all()
            if students:
                return {
                    'code': 0,
                    'msg': '查询学生成功',
                    'data': student_schema.dump(students, many=True)
                }
            else:
                return {
                    'code': 0,
                    'msg': '学生列表为空',
                }
        else:
            students = StuModel.query.filter_by(name=search).order_by("student_id").all()
            if students:
                return {
                    'code': 0,
                    'msg': '查询学生成功',
                    'data': student_schema.dump(students, many=True)
                }
            else:
                return {
                    'code': 0,
                    'msg': '未查询到学生',
                }
    else:
        student = StuModel.query.filter_by(student_id=student_id).first()
        if student:
            return {
                'code': 0,
                'msg': '查询学生成功',
                'data': student_schema.dump(student)
            }
        else:
            return {
                'code': 0,
                'msg': '未查询到该学生'
            }


@bp.route("/course/", methods=['POST', ])
@login_admin
def add_course():
    data = request.form
    try:
        course = course_schema.load(data)
        course.save_to_db()
        return {
            'code': 0,
            'msg': '添加课程成功'
        }
    except ValidationError as e:
        return {
            'code': 1,
            'msg': e.messages
        }


@bp.route("/course/<course_id>", methods=['DELETE', ])
@login_admin
def delete_course(course_id):
    course = CourseModel.query.filter_by(course_id=course_id).first()
    if course:
        # 删除课程下的学生
        stu_course = StuToCourse.query.filter_by(course_id=course_id).all()
        if stu_course:
            for i in stu_course:
                i.delete_from_db()
        course.delete_from_db()
        return {
            'code': 0,
            'msg': '删除课程成功'
        }
    else:
        return {
            'code': 1,
            'msg': '删除课程失败'
        }


@bp.route("/course/<course_id>", methods=['PUT', ])
@login_admin
def edit_course(course_id):
    course = CourseModel.query.filter_by(course_id=course_id).first()
    if course:
        data = request.form
        form = editcourseForm(data)
        if form.validate():
            for column in course.__table__.columns:
                if column.name  not in ('course_id' , 'updated' , 'id' , 'created'): setattr(course, column.name, data.get(column.name))
            course.save_to_db()
            return {
                'code': 0,
                'msg': '修改课程成功'
            }
        else:
            return {
                'code': 1,
                'msg': form.errors
            }
    else:
        return {
            'code': 1,
            'msg': '修改课程失败'
        }


@bp.route("/course/", defaults={'course_id': None}, methods=['GET', ])
@bp.route("/course/<course_id>", methods=['GET', ])
@login_admin
def get_course(course_id):
    if not course_id:
        search = request.args.get('search')
        if not search:
            courses = CourseModel.query.order_by('course_id').all()
            if courses:
                return {
                    'code': 0,
                    'msg': '查询课程成功',
                    'data': course_schema.dump(courses, many=True)
                }
            else:
                return {
                    'code': 0,
                    'msg': '课程列表为空'
                }
        else:
            courses = CourseModel.query.filter(
                db.or_(CourseModel.name.contains(search), CourseModel.desc.contains(search))).order_by(
                "course_id").all()
            if courses:
                return {
                    'code': 0,
                    'msg': '查询课程成功',
                    'data': course_schema.dump(courses, many=True)
                }
            else:
                return {
                    'code': 0,
                    'msg': '未查询到课程'
                }
    else:
        course = CourseModel.query.filter_by(course_id=course_id).first()
        if course:
            return {
                'code': 0,
                'msg': '查询课程成功',
                'data': course_schema.dump(course)
            }
        else:
            return {
                'code': 0,
                'msg': '未查询到该课程'
            }
