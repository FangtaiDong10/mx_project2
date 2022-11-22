import { createRouter, createWebHistory } from "vue-router";
import Layout from "../layout/index.vue";
import { useAuthStore } from "../stores/auth";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "layout",
      redirect: "/home",
      component: () => Layout,
      children: [
        {
          name: "home",
          path: "/home",
          component: () => import("../views/HomeView.vue"),
          meta: {
            title: "Home",
            requiresAuth: true,
          },
        },
        // {
        //   name: "courses",
        //   path: "/courses",
        //   component: () => import("../views/CoursesView.vue"),
        //   meta: {
        //     title: "Courses",
        //     requiresAuth: true,
        //   },
        // },
        {
          name: "browse",
          path: "/browse",
          component: () => import("../views/BrowseView.vue"),
          meta: {
            title: "All Courses",
            requiresAuth: true,
          },
        },
        {
          name: "orders",
          path: "/orders",
          component: () => import("../views/OrderView.vue"),
          meta: {
            title: "Orders",
            requiresAuth: true,
          }
        },
        {
          name: "browse_course",
          path: "/browse/:id",
          component: () => import("../views/CourseView.vue"),
          meta: { title: "Browse Course Page", requiresAuth: true },
        },
        {
          name: "course",
          path: "/courses/:id",
          component: () => import("../views/CourseView.vue"),
          meta: { title: "Course Page", requiresAuth: true },
        },
      ],
    },

    {
      path: "/login",
      name: "login",
      component: () => import("../views/LoginView.vue"),
    },

    {
      path: "/register",
      name: "register",
      component: () => import("../views/RegisterView.vue"),
    },
  ],
});

router.beforeEach((to) => {
  const authStore = useAuthStore();
  if (to.meta.requiresAuth === true && !authStore.isLoggedIn) {
    return {
      name: "login",
      query: { redirect: to.fullPath },
    };
  }
});

router.afterEach((to) => {
  document.title = to.meta.title || to.name;
});

export default router;
