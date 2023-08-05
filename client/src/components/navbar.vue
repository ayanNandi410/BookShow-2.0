<script>
import { onUpdated } from "vue";
import { RouterLink, RouterView, onBeforeRouteUpdate } from "vue-router";
import { mapState } from 'vuex'
import { logout_user, downloadVenueCSV } from '../api'
import axios from 'axios';

const API_URL = 'http://127.0.0.1:5000/api/'

export default {
  name: "navbar",
  data() {
    return {
      toastShow: false,
      header: "",
      head_end: "",
      message: "",
      type: "",
      notifications: [],
      selected: "",
    };
  },
  methods: {
    logoutCurrentUser(){
      this.$store.dispatch('toggle_current_user')
      localStorage.removeItem("auth_token");
      localStorage.removeItem("email");
      localStorage.removeItem("name");
      localStorage.removeItem("username");
      localStorage.removeItem("type");

      
      logout_user()
      .then(async res =>  {
          const data = await res.data
          this.toastShow = true;
          
          if(!res.ok){
            this.head_end = data.error_code;
            this.message = data.error_message;
            
          }
          else{
            this.venues = data;
            this.message = "Success";
            console.log("Successfully logged out...")
            this.type = "info";
          }
          
      })
      .catch(e => {
        this.message = e.data;
        console.log("Fetch Error: "+e)
        
    });   
    },

    downloadCSV(name){

      const btn = document.getElementById(name);

      axios({
        url: `${API_URL}venue/downloadCSV/${name}`, // Download File URL Goes Here
        method: 'GET',
        responseType: 'blob',
        headers: {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': ' GET, PUT, POST, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Origin, Content-Type, X-Auth-Token',
            'Access-Control-Allow-Credentials': 'false',
        },
    }).then((res) => {
        btn.innerHTML = "Download";
        btn.classList.remove('btn-primary');
        btn.classList.add('btn-success');

        var FILE = window.URL.createObjectURL(new Blob([res.data]));
        var docUrl = document.getElementById(name);
        docUrl.href = FILE;
        docUrl.setAttribute('download', name+'_Details.csv');
    });
    }

  },
computed: {
  userStatus(){
      return this.$store.state.active_user
    },
  userType(){
    return this.$store.state.user_type
  },
  setNotifications(){
    this.notifications = this.$store.state.notifications;
    return this.notifications;
  }
  },

  created() {
    localStorage.clear();
  },
};


</script>

<template>
  <nav
    class="navbar navbar-default navbar-expand-lg fixed-top"
    id="appNavbar"
    style="background-color: #9acbee;"
  >
    <a class="navbar-brand ms-4 me-4" href="#"
      ><img src="@/assets/boy-3d.png" width="50" height="50" />BookShow</a
    >

    <button
      class="navbar-toggler"
      type="button"
      data-bs-toggle="offcanvas"
      data-bs-target="#offcanvasNavbar"
      aria-controls="offcanvasNavbar"
    >
      <span class="navbar-toggler-icon"></span>
    </button>
    <div
      class="offcanvas offcanvas-end"
      tabindex="-1"
      id="offcanvasNavbar"
      aria-labelledby="offcanvasNavbarLabel"
    >
      <div class="offcanvas-header">
        <h5 class="offcanvas-title" id="offcanvasNavbarLabel">BookShow</h5>
        <button
          type="button"
          class="btn-close"
          data-bs-dismiss="offcanvas"
          aria-label="Close"
        ></button>
      </div>
      <div class="offcanvas-body">
        <ul class="navbar-nav justify-content-end flex-grow-1 pe-4">
          <li class="nav-item dropdown me-4 p-1" v-if="userStatus & userType=='admin'">

            <button class="btn dropdown-toggle" data-bs-toggle="dropdown" style="padding: 10% 20%;"
            data-bs-auto-close="outside" aria-expanded="false">
              <img src="@/assets/bell.svg"/>
              <span class="position-absolute top-0 start-100 badge rounded-pill bg-danger"
                  v-if="notifications.length!=0">{{ notifications.length }}</span>
            </button>
            <ul class="dropdown-menu p-3 text-body-secondary" style="max-width: 40%;">
              <li><p class="dropdown-header mb-0 pb-0">Notifications</p><hr/></li>
              <!-- <li><a class="dropdown-item" href="#">Action</a></li> -->
              <li v-for="item in setNotifications">
                <div style="font-size: 16px;">
                  CSV for Venue: {{ item.message }} ready
                  <a class="btn btn-sm btn-primary mt-2" style="padding: 2% 5%;" :id="item.message" @click="downloadCSV(item.message)">Get File</a>
                </div>
              </li>
            </ul>
          </li>

          <li class="nav-item" v-if="!userStatus">
            <router-link to="/" class="nav-link"
              ><img src="@/assets/home.svg" /> Home</router-link
            >
          </li>
          <li class="nav-item" v-if="userStatus & userType=='user'">
            <router-link to="/user/home" class="nav-link"
              ><img src="@/assets/home.svg" /> Home</router-link
            >
          </li>
          <li class="nav-item" v-if="userStatus & userType=='admin'">
            <router-link to="/admin/home" class="nav-link"
              ><img src="@/assets/home.svg" /> Home</router-link
            >
          </li>
          <li class="nav-item" v-if="!userStatus">
            <router-link to="/user/login" class="nav-link"
              ><img src="@/assets/login.svg" /> Login</router-link
            >
          </li>
          <li class="nav-item" v-if="!userStatus">
            <router-link to="/user/sign-up" class="nav-link"
              ><img src="@/assets/info.svg" /> Sign Up</router-link
            >
          </li>

          <li class="nav-item" v-if="userStatus & userType=='user'">
            <router-link to="/user/searchForVenues" class="nav-link"
              ><img src="@/assets/venue.svg" /> Venues</router-link
            >
          </li>
          <li class="nav-item" v-if="userStatus & userType=='user'">
            <router-link to="/user/shows" class="nav-link"
              ><img src="@/assets/movie.svg" /> Shows</router-link
            >
          </li>
          <li class="nav-item" v-if="userStatus & userType=='user'">
            <router-link to="/user/bookings" class="nav-link"
              ><img src="@/assets/calendar.svg" /> Bookings</router-link
            >
          </li>

          <li class="nav-item" v-if="userStatus & userType=='admin'">
            <router-link to="/admin/venues" class="nav-link"
              ><img src="@/assets/venue.svg" /> Venues</router-link
            >
          </li>
          <li class="nav-item" v-if="userStatus & userType=='admin'">
            <router-link to="/admin/shows" class="nav-link"
              ><img src="@/assets/movie.svg" /> Shows</router-link
            >
          </li>

          <li class="nav-item dropdown" v-if="userStatus">
            <a
              class="nav-link dropdown-toggle"
              href="#"
              role="button"
              data-bs-toggle="dropdown"
              aria-expanded="false"
            >
              Others
            </a>
            <ul class="dropdown-menu">
              <li v-if="userStatus & userType=='admin'">
                <router-link to="/admin/profile" class="dropdown-item"><img src="@/assets/person.svg" /> Profile</router-link>
              </li>
              <li v-if="userStatus & userType=='user'">
                <router-link to="/user/profile" class="dropdown-item"><img src="@/assets/person.svg" /> Profile</router-link>
              </li>
              <li v-if="userStatus">
                <hr class="dropdown-divider" />
              </li>
              <li v-if="userStatus">
                <router-link to="/?access=loggedOut" class="dropdown-item" @click="logoutCurrentUser"
              ><img src="@/assets/logout.svg" /> Logout</router-link
            >
              </li>
            </ul>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<style scoped>
  .router-link-active{
    background-color: rgb(81, 143, 202);
    border-radius: 10px;
    color: aliceblue;
  }
</style>
