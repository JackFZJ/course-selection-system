from flask import Flask
from project.extensions import db, ma, mg, cors, rpc,jwt
from project.blueprints import admin_bp, stu_bp
from project.jwt_operations import *
# 数据库迁移需要导入模型
import project.models as models 
import project.config as config
# import psycopg2
#其他包
# import gunicorn
# import gevent
# import pipreqs

#日志设置
# import log_init

app = Flask(__name__)
# app初始化
app.config.from_object(config.Config)
db.init_app(app)
mg.init_app(app, db)
# 在db绑定之后绑定
ma.init_app(app)
cors.init_app(app,supports_credentials=True)
rpc.init_app(app)
jwt.init_app(app)
# cors.init_app(app)

app.register_blueprint(admin_bp)
app.register_blueprint(stu_bp)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
