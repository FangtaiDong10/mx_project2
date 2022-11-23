from .model import User
from flask_jwt_extended import jwt_required, current_user
import functools


def permission_required(permission=None):
    def wrapper(func):
        @jwt_required()

        # 可以保留传入的func函数的参数，不会被装饰器函数覆盖
        @functools.wraps(func)
        def decorator(*args, **kwargs):
            
            # 如果用户没有登录，则抛出异常
            if current_user._cls == "User.Admin":
                if permission is None or permission in current_user.permissions:
                    return func(*args, **kwargs)
                else:
                    return {'message': f"Permission '{permission}' is required"}

            return {'message': "Permission denied"}, 403
        
        return decorator
    
    return wrapper



# taking the jwt manager from app instance
def register_user_lookup(jwt):

    def user_lookup_callback(jwt_header, jwt_payload):
        identity = jwt_payload['sub']
        return User.objects(username=identity).first_or_404(message="User not found")

    # use jwt user_lookup_loader function to activate the callback function
    jwt.user_lookup_loader(user_lookup_callback)
