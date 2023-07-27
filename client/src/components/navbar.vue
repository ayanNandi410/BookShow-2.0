<script>
import { RouterLink, RouterView } from "vue-router";
import { mapState } from 'vuex'

export default {
  name: "navbar",
  data() {
    return {
    };
  },
  methods: {
    logoutUser(){
      this.$store.dispatch('toggle_current_user')
    }
},
computed: {
  userStatus(){
      return this.$store.state.active_user
    }
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
          <li class="nav-item" v-if="!userStatus">
            <router-link to="/" class="nav-link"
              ><img src="@/assets/home.svg" /> Home</router-link
            >
          </li>
          <li class="nav-item" v-if="userStatus">
            <router-link to="/user/home" class="nav-link"
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
          <li class="nav-item" v-if="userStatus">
            <router-link to="/user/venues" class="nav-link"
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
              <li v-if="userStatus">
                <a class="dropdown-item" href="/user/userProfile"><img src="@/assets/person.svg" /> Profile</a>
              </li>
              <li v-if="userStatus">
                <hr class="dropdown-divider" />
              </li>
              <li v-if="userStatus">
                <router-link to="/user/login" class="dropdown-item" @click="logoutUser"
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
