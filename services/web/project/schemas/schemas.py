# --*--coding: utf-8 --*--
"""
序列化和反序列化
"""
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from project.models import AdminModel, StuModel, CourseModel
from marshmallow import post_load, fields, validate, validates_schema, ValidationError, validates
from werkzeug.security import generate_password_hash, check_password_hash
from project.extensions import db


class AdminSchema(SQLAlchemySchema):
    """模型构造器"""

    class Meta:
        model = AdminModel  # 模型类名
        # load_instance=True# 反序列化阶段时，直接返回模型对象
        sqla_session = db.session  # 构造器操作数据库的会话对象

    id = auto_field(dump_only=True)  # id自增，设置为只读字段就行
    name = auto_field(validate=validate.Length(min=1, max=20, error="用户名长度为1到20位"))
    password = auto_field(load_only=True,
                          validate=validate.Length(min=3, max=20, error="密码长度为6到20位"))  # 相当于只写字段 "write-only"
    password_confirm = fields.String()

    # 针对单个指定字段的值进行验证
    @validates("name")
    def validate_name(self, name):
        if AdminModel.query.filter_by(name=name).first():
            raise ValidationError("用户名已经被注册！")
        return name

    # 针对多个字段的验证
    @validates_schema
    def validate(self, data, **kwargs):
        if data["password"] != data["password_confirm"]:
            # 注意：验证失败以后，一定是raise抛出异常！！！不能是return!!!!
            raise ValidationError(field_name="password", message="密码和确认密码不一致！")
        return data

    @post_load
    def change_password(self, data, **kwargs):
        """反序列化钩子方法"""
        del data["password_confirm"]  # 删除掉不必要的字段
        data["password"] = generate_password_hash(data["password"])
        return AdminModel(**data)


class StudentSchema(SQLAlchemySchema):
    class Meta:
        model = StuModel
        sqla_session = db.session

    student_id = auto_field(validate=validate.Regexp('^\d{4}$', error='id为四位数字'))
    name = auto_field(validate=validate.Length(min=1, max=20, error="用户名长度为1到20位"))
    class_name = auto_field(validate=validate.Length(min=1, max=20, error="班级名长度为1到20位"))
    college_name = auto_field(validate=validate.Length(min=1, max=20, error="学院名长度为1到20位"))
    password = auto_field(load_only=True, validate=validate.Length(min=6, max=20, error="密码长度为6到20位"))
    password_confirm = fields.String()

    # 针对单个指定字段的值进行验证
    @validates("student_id")
    def validate_student_id(self, student_id):
        if StuModel.query.filter_by(student_id=student_id).first():
            raise ValidationError("学号已经被注册！")
        return student_id

    # 针对多个字段的验证
    @validates_schema
    def validate(self, data, **kwargs):
        if data["password"] != data["password_confirm"]:
            raise ValidationError(field_name="password", message="密码和确认密码不一致！")
        return data

    @post_load
    def change_password(self, data, **kwargs):
        """反序列化钩子方法"""
        del data["password_confirm"]  # 删除掉不必要的字段
        data["password"] = generate_password_hash(data["password"])
        return StuModel(**data)


class CourseSchema(SQLAlchemySchema):
    class Meta:
        model = CourseModel
        sqla_session = db.session
        load_instance = True  # 反序列化阶段时，直接返回模型对象

    course_id = auto_field(validate=validate.Regexp('^\d{4}$', error='id为四位数字'))
    name = auto_field(validate=validate.Length(min=1, max=20, error="课程名长度为1到20位"))
    desc = auto_field(validate=validate.Length(min=0, max=200, error="课程描述容量为0到200字符"))
    college_name = auto_field(validate=validate.Length(min=1, max=20, error="学院名长度为1到20位"))
    teacher_name = auto_field(validate=validate.Length(min=1, max=20, error="教师名长度为1到20位"))
    volume = auto_field(validate=validate.Range(min=0, max=10000, error="学生容量为0到10000"))
    score = auto_field(validate=validate.Range(min=0, max=20, error="学分为0到20"))
    time = auto_field(validate=validate.Range(min=0, max=200, error='学时为0到200'))

    # 针对单个指定字段的值进行验证
    @validates("course_id")
    def validate_student_id(self, course_id):
        # if request.method == 'POST' and CourseModel.query.filter_by(course_id=course_id).first():
        if CourseModel.query.filter_by(course_id=course_id).first():
            raise ValidationError("课程号已经被注册！")
        return course_id
