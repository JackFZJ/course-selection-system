from project.app import app
from project.models import *
from project.schemas import *
from werkzeug.security import check_password_hash, generate_password_hash
from marshmallow import ValidationError
from project.forms import *
from nameko.rpc import rpc, RpcProxy
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt
from datetime import datetime
from datetime import timezone

class services_admin(object):
    name = "services_admin"
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
    def admin_login(self,data):
        self.push_app_context()
        #  with app.app_context():
        admin = AdminModel.query.filter_by(name=data.get('name')).first()
        if admin and check_password_hash(admin.password, data.get('password')):
            # self.set_session(name='admin_name',value=admin.name)
            access_token = create_access_token(identity=admin.id,additional_claims={"is_admin": True})
            return {
                'code': 0,
                'msg': '登录成功',
                'access_token': access_token
            }
        else:
            return {
                'code': 1,
                'msg': '用户名或密码错误'
            }

    @rpc
    def admin_logout(self,jti):
        self.push_app_context()
        now = datetime.now(timezone.utc)
        db.session.add(TokenBlocklist(jti=jti, created_at=now))
        db.session.commit()
        return {'code':0,'msg':'注销成功'}
    
    @rpc
    def admin_add_student(self,data):
        app.app_context().push()
        try:
            student = self.student_schema.load(data)
            # student=StuModel(student_id='0068',name='test',password='abc123',class_name='xx9ban',college_name='xxxueyuan')
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

    @rpc
    def admin_delete_student(self,student_id):
        self.push_app_context()
        app.app_context().push()
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

    @rpc
    def admin_edit_student(self,student_id,data):
        self.push_app_context()
        student = StuModel.query.filter_by(student_id=student_id).first()
        if student:
            form = editstuForm(data=data)
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
                    # 'msg': 'xxx'
                }
        else:
            return {
                'code': 1,
                'msg': '修改学生失败'
            }

    @rpc
    def admin_get_student(self,student_id,search):
        self.push_app_context()
        if not student_id:
            if not search:
                students = StuModel.query.order_by("student_id").all()
                if students:
                    return {
                        'code': 0,
                        'msg': '查询学生成功',
                        'data': self.student_schema.dump(students, many=True)
                        # 'data': students
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
                        'data': self.student_schema.dump(students, many=True)
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
                    'data': self.student_schema.dump(student)
                }
            else:
                return {
                    'code': 0,
                    'msg': '未查询到该学生'
                }
    

    @rpc
    def admin_add_course(self,data):
        self.push_app_context()
        try:
            course = self.course_schema.load(data)
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
    
    @rpc
    def admin_delete_course(self,course_id):
        self.push_app_context()
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

    @rpc
    def admin_edit_course(self,course_id,data,validate_flag=False):
        self.push_app_context()
        course = CourseModel.query.filter_by(course_id=course_id).first()
        if course:
            if validate_flag:
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
                'msg': '修改课程失败'
            }

    @rpc
    def admin_get_course(self,course_id,search):
        self.push_app_context()
        if not course_id:
            
            if not search:
                courses = CourseModel.query.order_by('course_id').all()
                if courses:
                    return {
                        'code': 0,
                        'msg': '查询课程成功',
                        'data': self.course_schema.dump(courses, many=True)
                        # 'data': courses
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
                        'data': self.course_schema.dump(courses, many=True)
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
                    'data': self.course_schema.dump(course)
                }
            else:
                return {
                    'code': 0,
                    'msg': '未查询到该课程'
                }

    