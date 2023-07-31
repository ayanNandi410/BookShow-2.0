<script>

export default {
  name: "userHome",
  data() {
    return {
      auth_token: "",
    };
  },
  methods: {

  onMounted(){
    if(localStorage.auth_token){
      this.auth_token = localStorage.auth_token;
    }
    else{
        this.$router.push('/admin/login');
    }
  },

},
}
</script>

<template>
    <div class="body vh-100">
  <div class="container py-5 col-8">
    <div class="row">
      <div class="col-12 col-sm-8">
        <h1 class="display-5 fw-bold">User Profile</h1>
        <p class="col-md-8 fs-4"><br/>Name : <b>{{ }}</b><br/>Email : <b>{{  }}</b></p>
      </div>
      <div class="col-12 col-sm-4">
        <img src="@/assets/user.png" width="200" height="200">
      </div>
    </div>
  </div>
</div>
</template>