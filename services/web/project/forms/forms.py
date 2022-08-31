# --*--coding: utf-8 --*--
import wtforms
from wtforms.validators import length, EqualTo, Regexp, NumberRange

class editstuForm(wtforms.Form):
    name = wtforms.StringField(validators=[length(min=1, max=20, message="用户名长度为1到20位")])
    class_name = wtforms.StringField(validators=[length(min=1, max=20, message="班级名长度为1到20位")])
    college_name = wtforms.StringField(validators=[length(min=1, max=20, message="学院名长度为1到20位")])
    password = wtforms.StringField(validators=[length(min=6, max=20, message="密码长度为6到20位")])
    password_confirm = wtforms.StringField(validators=[EqualTo("password", message="两次输入的密码不一致")])


class editcourseForm(wtforms.Form):
    name = wtforms.StringField(validators=[length(min=1, max=20, message="课程名长度为1到20位")])
    desc = wtforms.StringField(validators=[length(min=0, max=200, message="课程描述容量为0到200字符")])
    time = wtforms.IntegerField(validators=[NumberRange(min=0, max=201, message="学时只能为0到200")])
    college_name = wtforms.StringField(validators=[length(min=1, max=20, message="课程名长度为1到20位")])
    teacher_name = wtforms.StringField(validators=[length(min=1, max=20, message="教师名长度为1到20位")])
    volume = wtforms.IntegerField(validators=[NumberRange(min=0, max=10000, message="学生容量为0到10000")])
    score = wtforms.FloatField(validators=[NumberRange(min=0, max=20, message="学分为0到20")])
