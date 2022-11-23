import datetime
from email import message
from flask_restx import Namespace, Resource
from flask import request, jsonify

from app.user import permission_required
from .model import Course, Lecture, LectureAttachment

from flask_jwt_extended import create_access_token, current_user, jwt_required
from ..utils import paginate,upload_file_to_s3
from datetime import datetime
import json

course_api = Namespace("courses")

@course_api.route("/")
class CourseListApi(Resource):
    # @permission_required()
    @jwt_required()
    def get(self):
        query = {}
        if "campus" in request.args:
            query["campus"] = request.args["campus"]

        page = request.args.get("page", 1, int)

        return paginate(Course.objects(**query), page)

    @permission_required()
    def post(self):
        # convert JSON data to document instance
        course = Course.from_json(request.data)
        course.save()
        return course.to_dict(), 201

@course_api.route("/<course_id>")
class CourseApi(Resource):
    @jwt_required()
    def get(self, course_id):
        course = Course.objects(id=course_id).first_or_404()
        return course.to_dict()



@course_api.route("/<course_id>/lectures")
class LectureListApi(Resource):
    # @permission_required("lecture_admin")
    @jwt_required()
    def post(self, course_id):
        course = Course.objects(id=course_id).first_or_404()

        data = request.json

        if "scheduled_time" in data:
            data["scheduled_time"] = datetime.fromisoformat(data["scheduled_time"])
            

        # generate Lecture instance structure
        lecture = Lecture(**data)
        course.lectures.append(lecture)
        
        course.save()
        return lecture.to_dict(), 201

    @jwt_required()
    def get(self, course_id):
        course = Course.objects(id=course_id).first_or_404()

        if current_user._cls == "User.Student":
            print(course.enrolled_students)
            if current_user not in course.enrolled_students:
                return {"messege": "You are not allowed to access this course"}, 403
        
        return [lecture.to_dict() for lecture in course.lectures]


# for uploading the attachment by the teacher
@course_api.route("/<course_id>/lectures/<lecture_id>/attachments")
class LectureAttachmentListApi(Resource):
    # @permission_required("lecture_admin")
    jwt_required()
    def post(self, course_id, lecture_id):
        course = Course.objects(id=course_id).first_or_404()
        
        # original api therefore no first_or_404
        lecture = course.lectures.filter(id=lecture_id).first()

        if lecture is None:
            return {"message": "lecture not exists"}, 404
        
        # if the lecture exists, then the attachment should be uploaded
        uploaded_file = request.files.get("file")

        if uploaded_file is None:
            return {"message": "No file uploaded"}, 400

        if uploaded_file.filename in [attachment.filename for attachment in lecture.attachments]:
            return {"message": "File already exists"}, 409
        
        # Upload logic
        attachment = LectureAttachment(
            **json.loads(request.form.get("metadata", default={})), 
            filename = uploaded_file.filename
        )

        # after creating the attachment, we need to upload the file to s3 (gets the file from frontend, and store in the pseudo path in S3)
        attachment.bucket_url = upload_file_to_s3(uploaded_file, f"lectures/{lecture_id}/attachments")

        lecture.attachments.append(attachment)

        course.save()
        # print(uploaded_file)
        return attachment.to_dict() , 201


@course_api.route("/<course_id>/lectures/<lecture_id>/attachments/<filename>")
class LectureAttachmentApi(Resource):
    # delete the specific attachment
    @permission_required("lecture_admin")
    def delete(self, course_id, lecture_id,filename):
        course = Course.objects(id=course_id).first_or_404()
        lecture = course.lectures.filter(id=lecture_id).first()

        if lecture is None:
            return {"message": "lecture not exists"}, 404
        
        del_num = lecture.attachments.filter(filename=filename).delete()

        course.save()

        return del_num , 200