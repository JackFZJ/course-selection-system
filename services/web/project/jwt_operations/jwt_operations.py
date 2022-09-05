from project.extensions import jwt,db
from project.models import StuModel,TokenBlocklist,AdminModel


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    student=StuModel.query.filter_by(id=identity).one_or_none()
    if student:
        return student
    admin=AdminModel.query.filter_by(id=identity).one_or_none()
    if admin:
        return admin
    return None

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()

    return token is not None

#重写jwt错误信息
#令牌过期
@jwt.expired_token_loader
def my_expired_token_callback(jwt_header, jwt_payload):
    return {'code':1, 'msg':"令牌过期，请重新登录"}, 401

@jwt.revoked_token_loader
def my_revoked_token_callback(jwt_header, jwt_payload):
    return {'code':1,'msg':"令牌已注销"},403

@jwt.user_lookup_error_loader
def my_user_lookup_error_callback(jwt_header, jwt_payload):
    return {'code':1,'msg':"用户未登录"},401

@jwt.unauthorized_loader
def my_unauthorized_error_callback(error_msg):
    return {'code':1,'msg':"用户未登录，请求头无令牌"},401