<script>
import ToastMsg from '../components/toastMsg.vue';

export default {
  name: "startHome",
  data() {
    return {
      header: "",
      message: "",
      head_end: "",
      type: "",
      toastShow: false,
    };
  },
  mounted(){
    console.log(this.$route.query.access);
    if(this.$route.query.access)
    {
      this.message = "Logged out successfully...";
      this.header = "Logout";
      this.type = "info"
      this.toastShow = true;
    }
  },
  
  methods: {

  closeToast(){
      this.toastShow = false;
  },
  },

  components: { ToastMsg },
};
</script>

<template>
  <div class="container text-center" style="height: 100vh">
    <ToastMsg 
    v-bind:header="header" 
    v-bind:head_end="head_end" 
    v-bind:message="message" 
    v-bind:type="type" 
    v-if="toastShow"
    @close-toast="closeToast" />

    <div class="row justify-content-md-center" style="margin-top: 10%">
      <div class="col-10 col-md-4 mb-3">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">Admin User</h5>
            <p class="card-text">Login to work on shows and venues</p>
            <router-link to="/admin/login" class="btn btn-primary"
              >Admin Login</router-link
            >
          </div>
        </div>
      </div>
      <div class="col-10 col-md-4 mb-3">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">General User</h5>
            <p class="card-text">
              Login to buy tickets and learn about the latest shows
            </p>
            <router-link to="/user/login" class="btn btn-primary"
              >User Login</router-link
            >
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
