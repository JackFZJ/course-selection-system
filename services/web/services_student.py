from nameko.rpc import rpc, RpcProxy
from project.models import *
from project.schemas import *
from werkzeug.security import check_password_hash, generate_password_hash
from marshmallow import ValidationError
from project.forms import *
from project.app import app
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt
from datetime import datetime
from datetime import timezone


class services_student(object):
    name = "services_student"
    
    # register_rpc = RpcProxy("index")

    app.app_context().push()
    app.config['SQLALCHEMY_DATABASE_URI']='postgresql://hello_flask:123456@db:5432/course_system_prod'
    admin_schema = AdminSchema()
    student_schema = StudentSchema()
    course_schema = CourseSchema()

    def push_app_context(self):
        app.app_context().push()

    @rpc
    def index(self):
        self.push_app_context()
        return {'welcome_info': "欢迎使用Python微服务"}

    @rpc
    def student_login(self,data):
        self.push_app_context()
        student = StuModel.query.filter_by(student_id=data.get('id')).first()
        if student and check_password_hash(student.password, data.get('password')):
            access_token = create_access_token(identity=student.id,additional_claims={"is_student": True})
            return {
                'code': 0,
                'msg': '登录成功',
                'access_token': access_token
            }
        else:
            return {
                'code': 1,
                'msg': '学号或密码错误'
            }
    
    @rpc
    def student_logout(self,jti):
        self.push_app_context()
        now = datetime.now(timezone.utc)
        db.session.add(TokenBlocklist(jti=jti, created_at=now))
        db.session.commit()
        return {'code':0,'msg':'注销成功'}

    @rpc
    def student_get_courses(self,student_id,search):
        self.push_app_context()
        stu_courses = StuToCourse.query.filter_by(student_id=student_id).order_by("course_id").all()
        
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
                # 'data': course_schema.dump(courses, many=True)
                'data': self.course_schema.dump(courses, many=True)
            }
        else:
            return {
                'code': 0,
                'msg': '没有可选课程'
            }

    @rpc
    def student_get_selected_courses(self,student_id):
        self.push_app_context()
        subq = db.session.query(StuToCourse.course_id.label('cid')).filter(StuToCourse.student_id == student_id).subquery()
        courses = CourseModel.query.filter(CourseModel.course_id == subq.c.cid).order_by("course_id").all()
        if courses:
            return {
                'code': 0,
                'msg': '查询已选课程成功',
                # 'data': course_schema.dump(courses, many=True)
                'data': self.course_schema.dump(courses, many=True)
            }
        else:
            return {
                'code': 0,
                'msg': '没有已选课程'
            }

    @rpc
    def student_select_course(self,student_id,course_id):
        self.push_app_context()
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

    @rpc
    def student_drop_course(self,course_id,student_id):
        self.push_app_context()
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