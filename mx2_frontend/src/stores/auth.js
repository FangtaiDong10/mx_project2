import axios from "../utils/http";
import { getUser } from "../api/user";
import { defineStore } from "pinia";

// prevent the name from being used as a variable
const prefix = import.meta.env.VITE_STORAGE_PREFIX;

export const useAuthStore = defineStore({
  id: "auth",
  // data will be stored in state
  state: () => ({
    token: localStorage.getItem(prefix + "token"),
    userInfo: JSON.parse(localStorage.getItem(prefix + "user_info")),
  }),

  getters: {
    // real time state data will be getted from defined methods
    getToken: (state) => state.token,
    getUserInfo: (state) => state.userInfo,
    isLoggedIn: (state) => !!state.token,
  },

  actions: {
    async login(username, password) {
      const response = await axios.post("auth/login", { username, password });
      
      const { data } = response;
      const userInfo = data.user;
      if (userInfo.enrolled_courses === undefined) {
        userInfo.enrolled_courses = [];
      }



      localStorage.setItem(prefix + "token", data.token);
      localStorage.setItem(prefix + "user_info", JSON.stringify(userInfo));
      this.token = data.token;
      this.userInfo = userInfo;
    },
    async reload() {
      // based on current username to refresh userInfo
      this.userInfo = await getUser(this.userInfo.username);
    },
    async logout() {
      localStorage.removeItem(prefix + "token");
      localStorage.removeItem(prefix + "user_info");
      this.token = null;
      this.userInfo = null;
    },
  },
});
