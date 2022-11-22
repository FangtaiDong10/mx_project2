import axios from "../utils/http";

export const getUser = async (username) => {
  const response = await axios.get("/users/" + username);
  // console.log(response.data);

  return response.data;
};

export const createStudent = async (user) => {
  // axio post can automatically convert the second parameter to JSON
  const response = await axios.post("/students/", user);
  return response.data;
}