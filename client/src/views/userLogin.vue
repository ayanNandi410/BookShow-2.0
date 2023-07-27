<script> 
export default {
  name: "UserLogin",
  data() {
    return {
      email: "",
      password: "",
    };
  },
  methods: {
    isValidEmail() {
      return /^[^@]+@\w+(\.\w+)+\w$/.test(this.email);
    },

    submitForm() {

      if(!this.isValidEmail()){
          console.log("Invalid email");
      }

      this.$store.dispatch('load_auth_token', { email: this.email, password: this.password })
      this.$store.dispatch('toggle_current_user')
      this.$router.push('/user/home')
    },
  },
  computed: {

  },
  components: {},
};
</script>

<template>
  <div class="body">
    <div class="container-fluid">
      <div class="row d-flex justify-content-center">
        <div class="col-md-9 col-lg-6 col-xl-5">
          <div class="card" style="width: 25rem">
            <img
              src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-login-form/draw2.webp"
              class="card-img-top"
              alt="Sample image"
            />
            <div class="card-body">
              <h5 class="card-title">Sign In</h5>
              <p class="card-text">
                Enter your details to login and access awesome shows
              </p>
              <p class="small fw-bold mt-2 pt-1 mb-0">
                Don't have an account?
                <a href="/userSignup" class="link-danger">Register</a>
              </p>
            </div>
          </div>
        </div>
        <div class="col-md-8 col-lg-6 col-xl-4 offset-xl-1">
          <!-- <form class="mt-4" method="get"> -->
            <h3 class="alert alert-primary mb-4">Enter Details</h3>
            <!-- Email input -->
            <div class="form-floating mb-4">
              <input
                type="email"
                id="login_email"
                name="login_email"
                v-model="email"
                class="form-control form-control-lg"
                placeholder="Enter a valid email address"
              />
              <label class="form-label" for="form3Example3"
                >Email address</label
              >
            </div>

            <!-- Password input -->
            <div class="form-floating mb-3">
              <input
                type="password"
                id="login_passwd"
                name="login_passwd"
                v-model="password"
                class="form-control form-control-lg"
                placeholder="Enter password"
              />
              <label class="form-label" for="form3Example4">Password</label>
            </div>

            <div class="d-flex justify-content-between align-items-center">
              <!-- Checkbox -->
              <div class="form-check mb-0">
                <input
                  class="form-check-input me-2"
                  type="checkbox"
                  value=""
                  id="login_remember"
                  name="login_remember"
                />
                <label class="form-check-label" for="form2Example3">
                  Remember me
                </label>
              </div>
            </div>

            <div class="d-flex justify-content-center text-lg-start mt-4 pt-2">
              <button
                @click="submitForm"
                class="btn btn-primary btn-lg"
                style="padding-left: 2.5rem; padding-right: 2.5rem"
              >
                Login
              </button>
            </div>
          <!-- </form> -->
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
