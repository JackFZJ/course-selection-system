# --*--coding: utf-8 --*--
"""
重置数据库，并添加几条测试数据的脚本
"""
from project.extensions import db
from app import app
from project.models import AdminModel, StuModel, CourseModel
from werkzeug.security import generate_password_hash

with app.app_context():
    db.drop_all()
    db.create_all()
    #
    """
    生成一个管理员：
    账号：admin
    密码：123456
    """
    admin1 = AdminModel(name='admin', password=generate_password_hash('123456'))
    stu1 = StuModel(student_id="0058", name="张三", password=generate_password_hash('abc123'), class_name="控制9班",
                    college_name="信息学院")
    stu2 = StuModel(student_id="0100", name="李四", password=generate_password_hash('abc123'), class_name="机设8班",
                    college_name="机械学院")
    cou1 = CourseModel(course_id="1001", name="控制原理", desc="信息学院课程1", time="64", college_name="信息学院",
                       teacher_name="信息老师", volume=50, score=2, students=[stu1, ])
    cou2 = CourseModel(course_id="1002", name="机械原理", desc="xx学院课程1", time="32", college_name="机械学院",
                       teacher_name="机械老师", volume=1, score=1.5, students=[stu2, ])
    db.session.add(admin1)
    db.session.add(stu1)
    db.session.add(stu2)
    db.session.add(cou1)
    db.session.add(cou2)

    db.session.commit()

    # 从数据库中打印账号和密码
    data = AdminModel.query.filter_by(name='admin').first()
    print('name:' + data.name)
    print('password:' + data.password)
