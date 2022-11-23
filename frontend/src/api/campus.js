import axios from "../utils/http";

export const getCampusList = async () => {
  const response = await axios.get("/campus/");
  // console.log(response.data);

  return response.data;
};
