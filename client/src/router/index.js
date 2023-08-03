import { createRouter, createWebHistory } from "vue-router";
import Ping from "../views/Ping.vue";
import startHome from "../views/startHome.vue";
import adminLogin from "../views/adminLogin.vue";
import userLogin from "../views/userLogin.vue";
import userSignup from "../views/userSignup.vue";


function guardMyroute(to, from, next)
{
 var isAuthenticated= false;

  if(localStorage.auth_token)
    isAuthenticated = true;
  else
    isAuthenticated= false; 
  
  if(isAuthenticated) 
  {
    next(); // allow to enter route
  } 
  else
  {
    next({ path: '/user/login', query: { access:'invalid' }}); // go to '/login';
  }
}


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [

    //Testing
    {
      path: "/ping",
      name: "ping",
      component: Ping,
    },


    //Anonymous Routes
    {
      path: "/",
      name: "home",
      component: startHome,
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
      path: "/admin/login",
      name: "adminLogin",
      component: adminLogin,
    },

    // User routes
    {
      path: "/user/home",
      name: "userHome",
      beforeEnter : guardMyroute,
      component: () => import ("../views/userHome.vue"),
    },
    {
      path: "/user/searchForVenues",
      name: "userSearchVenues",
      beforeEnter : guardMyroute,
      component: () => import ("../views/userSearchVenues.vue"),
    },
    {
      path: "/user/venue/home",
      name: "userVenueHome",
      beforeEnter : guardMyroute,
      component: () => import ("../views/userVenueHome.vue"),
      props: true,
    },
    {
      path: "/user/profile",
      name: "userProfile",
      beforeEnter : guardMyroute,
      component: () => import ("../views/userProfile.vue"),
    },

    {
      path: "/user/venues/forCity/:city",
      name: "userVenues",
      beforeEnter : guardMyroute,
      component: () => import ("../views/userVenues.vue"),
    },
    {
      path: "/user/bookings",
      name: "userBookings",
      beforeEnter : guardMyroute,
      component: () => import ("../views/userBookings.vue"),
    },

    
    // Admin Routes
    {
      path: "/admin/home",
      name: "adminHome",
      beforeEnter : guardMyroute,
      component: () => import('../views/adminHome.vue'),
    },
    {
      path: "/admin/profile",
      name: "adminProfile",
      beforeEnter : guardMyroute,
      component: () => import ("../views/adminProfile.vue"),
    },
    {
      path: "/admin/venues",
      name: "adminVenues",
      beforeEnter : guardMyroute,
      component: () => import('../views/adminVenues.vue'),
    },
    {
      path: "/admin/shows",
      name: "adminShows",
      beforeEnter : guardMyroute,
      component: () => import('../views/adminShows.vue'),
    },
    {
      path: "/admin/venue/add",
      name: "addVenue",
      beforeEnter : guardMyroute,
      component: () => import('../views/addVenue.vue'),
    },
    {
      path: "/admin/show/add",
      name: "addShow",
      beforeEnter : guardMyroute,
      component: () => import('../views/addShow.vue'),
    },
    {
      path: "/admin/timings/view",
      name: "displayTimings",
      beforeEnter : guardMyroute,
      component: () => import('../views/adminTimings.vue'),
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
