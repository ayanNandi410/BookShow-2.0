import { createRouter, createWebHistory } from "vue-router";
import Ping from "../views/Ping.vue";
import startHome from "../views/startHome.vue";
import adminLogin from "../views/adminLogin.vue";
import userLogin from "../views/userLogin.vue";
import userSignup from "../views/userSignup.vue";
import userHome from "../views/userHome.vue"

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: startHome,
    },
    {
      path: "/user/home",
      name: "userHome",
      component: () => import ("../views/userHome.vue"),
    },
    {
      path: "/admin/login",
      name: "adminLogin",
      component: adminLogin,
    },
    {
      path: "/user/login",
      name: "userLogin",
      component: userLogin,
    },
    {
      path: "/user/sign-up",
      name: "userSignup",
      component: userSignup,
    },
    {
      path: "/ping",
      name: "ping",
      component: Ping,
    },
    {
      path: "/user/venues/forCity/:city",
      name: "userVenues",
      component: () => import ("../views/userVenues.vue"),
    },
  ],
});

export default router;

/*
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    }
*/
