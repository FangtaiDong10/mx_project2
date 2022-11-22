import datetime
from email import message
from flask_restx import Namespace, Resource
from flask import request
from app import user

from flask_jwt_extended import create_access_token, current_user, jwt_required
from app.user import permission_required
from .model import User, Admin, Student, Teacher, check_password, get_hash_password
from ..campus.model import Campus
from ..utils import paginate

auth_api = Namespace('auth', description='Authentication related operations')
# auth_api
@auth_api.route('/login')
class login(Resource):
    # post contain request body(username and password)
    def post(self):
        username = request.json.get('username')
        password = request.json.get('password')

        if not username or not password:
            return {'message': 'username or password is missing'}, 400

        # find the user in the database
        user = User.objects(username=username).first_or_404(
            message="User not found")

        if not check_password(password, user.password):
            # authentication failed
            return {'message': 'password is incorrect'}, 401

        jwt_token = create_access_token(
            identity=user.username, expires_delta=datetime.timedelta(days=30))

        # create a response containing the token
        return {"user": user.to_dict(), "token": jwt_token}, 201






# user_api of User List
user_api = Namespace('users', description='User related operations')
@user_api.route('/')
class UserList(Resource):
    # @jwt_required()
    @permission_required()
    def get(self):

        obj_cls = User

        if "user_type" in request.args:
            user_type = request.args["user_type"]

            if user_type == "admin":
                obj_cls = Admin
            elif user_type == "student":
                obj_cls = Student
            elif user_type == "teacher":
                obj_cls = Teacher

        # return [user.to_dict() for user in obj_cls.objects()], 200

        # List of filters
        query = {}
        if "campus" in request.args:
            query["campus"] = request.args["campus"]

        page = request.args.get('page', 1, type=int)

        return paginate(obj_cls.objects(**query), page_num=page)


# enquiry a specific user by user_id
# users won't duplicate in the database
@user_api.route("/<username>")
class UserApi(Resource):
    @jwt_required()
    def get(self, username):
        if username != current_user.username and not isinstance(current_user, Admin):
            return {"message": "permission denied"}, 403

        return (
            User.objects(username=username).first_or_404(
                message="User not found").to_dict()
        )
    @permission_required()
    def delete(self, username):
        user = User.objects(username=username).first_or_404(message="User not found")
        if isinstance(current_user, Admin) and "sys_owner" not in current_user.permissions:
            return {"message": "permission denied"}, 403
        
        user.delete()
        
        # usally we return a count of deleted objects
        return user.to_dict(), 200






student_api = Namespace('students', description='Student related operations')
@student_api.route('/')
class StudentList(Resource):
    def post(self):
        request_data = request.json
        request_data['password'] = get_hash_password(request_data['password'])
        request_data['campus'] = Campus.objects(
            id=request_data['campus']).first_or_404("Campus not found")
        # from_json() api using to JSON string
        student = Student(**request_data)
        student.save()
        return student.to_dict(), 201


admin_api = Namespace('admins', description='Admin related operations')
@admin_api.route('/')
class AdminList(Resource):
    @permission_required('system_owner')
    def post(self):
        request_data = request.json
        request_data['password'] = get_hash_password(request_data['password'])
        request_data['campus'] = Campus.objects(
            id=request_data['campus']).first_or_404("Campus not found")
        admin = Admin(**request_data)
        admin.save()
        return admin.to_dict(), 201


teacher_api = Namespace('teachers', description='Teacher related operations')
@teacher_api.route('/')
class TeacherList(Resource):
    @permission_required()
    def post(self):
        request_data = request.json
        request_data['password'] = get_hash_password(request_data['password'])
        request_data['campus'] = Campus.objects(
            id=request_data['campus']).first_or_404("Campus not found")
        teacher = Teacher(**request_data)
        teacher.save()
        return teacher.to_dict(), 201
