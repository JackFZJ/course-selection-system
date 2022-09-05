# --*--coding: utf-8 --*--
from datetime import datetime

from project.extensions import db
from sqlalchemy.dialects.postgresql import UUID
import uuid
"""
ForeignKey表示，Addresses.user_id列的值应该等于users.id列中的值，即，users的主键
relationship(), 它告诉 ORM ,Address类本身应该使用属性Address.user链接到User类
relationship()的参数中有一个称为backref()的relationship()的子函数，反向提供详细的信息, 即在users中添加User对应的Address对象的集合，保存在User.addresses中
Address.user和User.addresses被称为一个双向互补关系,，并且这是SQLAlchemy ORM的一个关键特性。
"""
class DbOperate(object):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid1)
    created = db.Column(db.DateTime, default=datetime.now,nullable=False)
    updated = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now,nullable=False)
    def save_to_db(self):  # 添加到数据库中 -- 后面会使用到
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):  # 从数据库中删除该记录
        db.session.delete(self)
        db.session.commit()

class AdminModel(db.Model,DbOperate):
    __tablename__ = "admins"
    name = db.Column(db.String(32), nullable=False, unique=True)
    password=db.Column(db.String(200),nullable=False)

class StuToCourse(db.Model,DbOperate):
    __tablename__="stu_to_course"
    student_id=db.Column(db.String(32),db.ForeignKey("students.student_id"))
    course_id=db.Column(db.String(32),db.ForeignKey("courses.course_id"))

class StuModel(db.Model,DbOperate):
    __tablename__="students"
    student_id = db.Column(db.String(32), unique=True)
    name = db.Column(db.String(32), nullable=False, unique=False)
    password = db.Column(db.String(200), nullable=False)
    class_name = db.Column(db.String(32), nullable=False)
    college_name = db.Column(db.String(32), nullable=False)

    courses = db.relationship("CourseModel",secondary="stu_to_course", backref="students")

class CourseModel(db.Model,DbOperate):
    __tablename__="courses"
    course_id = db.Column(db.String(32), unique=True)
    name = db.Column(db.String(32), nullable=False, unique=False)
    desc=db.Column(db.Text,nullable=True)
    time = db.Column(db.Integer, nullable=False)
    college_name = db.Column(db.String(32), nullable=False)
    teacher_name = db.Column(db.String(32), nullable=False)
    volume = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Float, nullable=False)

class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False)
