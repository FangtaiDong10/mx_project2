import axios from "../utils/http";

// show all orders information
export const getOrders = async (page = 1, paid = null) => {
  const params = {
    page,
    paid,
  };
  const response = await axios.get("/orders/", { params });
  return response.data;
};

// create an order
export const createOrder = async (courseId) => {
  const response = await axios.post("/orders/", { course: courseId });
  return response.data;
};

export const payOrder = async (orderId, paidPrice, paidComment) => {
  const response = await axios.post(`/orders/${orderId}/paid`, {
    paid_price: paidPrice,
    paid_comment: paidComment,
    paid_time: new Date().toISOString().slice(0, -1),
  });
  return response.data;
};
