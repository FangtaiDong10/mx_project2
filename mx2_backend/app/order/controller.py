from flask import request
from flask_restx import Namespace, Resource

from app.user import permission_required
from flask_jwt_extended import create_access_token, current_user, jwt_required
from ..utils import paginate

from .model import Order
from datetime import datetime

order_api = Namespace("orders")

@order_api.route("/")
class OrderListApi(Resource):
  # user need login first
  @jwt_required()
  def post(self):
    order: Order = Order.from_json(request.data)
    if (current_user._cls != "User.Admin" or "order_admin" not in current_user.permissions):
      order.student = current_user.to_dbref()
    
 
    order.original_price = order.course.original_price

    order.save()
    return order.to_dict(), 201

  @jwt_required()
  def get(self):
    page_num = request.args.get("page", 1, int)
    query = {}

    # filter whether the user paid for the course
    if "paid" in request.args:
      query["paid"] = request.args.get("paid").lower() == "true"
    
    # current_user is not admin 
    if (current_user._cls != "User.Admin" or "order_admin" not in current_user.permissions):
      query["student"] = current_user.id

    # need to be fixed when admin logged in
    
    return paginate(Order.objects(**query), page_num=page_num)

@order_api.route("/<order_id>")
class OrderApi(Resource):
  @permission_required("order_admin")
  def delete(self, order_id):
    order = Order.objects(id=order_id).first_or_404()
    order.delete()

    return order.to_dict(), 200

  @jwt_required()
  def get(self, order_id):
    if (current_user._cls != "User.Admin" or "order_admin" not in current_user.permissions):
      
      order = Order.objects(id=order_id).first_or_404()

      if order.student.id != current_user.id:
        return {"message": "permission denied"}, 403
    else:
      order = Order.objects(id=order_id).first_or_404()
    
    return order.to_dict(), 200
        
@order_api.route("/<order_id>/paid")
class OrderPaidApi(Resource):
  # @permission_required("order_admin")
  @jwt_required()
  def post(self, order_id):
    order = Order.objects(id=order_id).first_or_404()
    
    data = request.json
    
    if "paid_time" in request.json:
      order.paid_time = datetime.fromisoformat(data["paid_time"])
      del data["paid_time"]

    order.update(**data)
    order.paid = True
    order.student.enrolled_courses.append(order.course)
    order.student.save()
    order.course.enrolled_students.append(order.student)
    order.course.save()
    
    order.save()
    return order.to_dict(), 200