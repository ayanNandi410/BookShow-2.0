
<script> 
import ToastMsg from '../components/toastMsg.vue'
import { fetch_auth_token, logout_user } from '../api';
import { onMounted, onUpdated } from 'vue';


export default {
  name: "UserLogin",
  data() {
    return {
      user_details: {},
      email: "",
      password: "",
      header: "",
      head_end: "",
      message: "",
      type: "",
      toastShow: false,
    };
  },

  mounted() {
    if(this.$route.query.access)
    {
      this.message = "Please login first...";
      this.header = "Invalid Access";
      this.toastShow = true;
    }
  },

  methods: {
    isValidEmail() {
      return /^[^@]+@\w+(\.\w+)+\w$/.test(this.email);
    },

    closeToast(){
      this.toastShow = false;
    },

    invalid_logout(){
      this.type = "error"
      this.message = "Admin Login not allowed";
      this.header = "Validation Error";

      // this.$store.dispatch('toggle_current_user');
      
      logout_user()
        .then(async res => {
          const data = await res.data
          this.toastShow = true;

          if (!res.ok) {
            this.head_end = data.error_code;
            this.message = data.error_message;

          }
          else {
            console.log("Successfully logged out...")
          }

        })
        .catch(e => {
          this.message = e.data;
          console.log("Fetch Error: " + e)

        });
    },

    setLocalStorage(data){
      localStorage.auth_token = data['response']['user']['authentication_token'];
      localStorage.name = data['response']['user']['name'];
      localStorage.username = data['response']['user']['username'];
      localStorage.email = this.email;
      localStorage.type = "user";
    },

    submitForm() {
      this.type = "info";
      this.toastShow = true;
      this.header = "Logging in...";

      if(!this.isValidEmail()){
          console.log("Invalid email");
          this.type = "error";
          this.message = "Invalid email";
          this.header = "Form Error";
      }
      else if(this.password.length < 8){
        console.log("Password Length too short");
        this.type = "error";
        this.message = "Password Length too short";
        this.header = "Form Error";
      }
      else{

        fetch_auth_token({ email: this.email, password: this.password })
        .then(async res =>  {
            const data = await res.json()

            if(!res.ok){
              this.type = "error"
              this.message = data.response.errors[0];
              this.header = "Validation Error";
            }
            else{
                const isAdmin = data['response']['user']['isAdmin'];

                if(isAdmin){
                  this.invalid_logout();
                }
                else{
                  
                  this.user_details = {
                    auth_token: data['response']['user']['authentication_token'],
                    name: data['response']['user']['name'],
                    username: data['response']['user']['username'],
                    email: this.email,
                    type: "user",
                  };

                  this.setLocalStorage(data);

                  this.$store.commit('set_user_details', this.user_details);

                  this.$store.commit('toggle_user')
                  this.$router.replace('/user/home')
                  this.toastShow = false;
                  this.$store.commit('empty_error_message')
                }
            }
            
        })
        .catch(e => {
            this.type = "error"
            this.message = e.message;
            this.header = "Fetch Error"
            }
        );   
        
      }
    },
  },
  components: { ToastMsg },

};
</script>

<template>
  <div class="body container">
    <ToastMsg 
    v-bind:header="header" 
    v-bind:head_end="head_end" 
    v-bind:message="message" 
    v-bind:type="type" 
    v-if="toastShow"
    @close-toast="closeToast" />

    <div class="container-fluid">
      <div class="row d-flex justify-content-center">
        <div class="col-md-9 col-lg-6 col-xl-5 mb-2">
          <div class="card" style="width: 25rem">
            <img
              src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-login-form/draw2.webp"
              class="card-img-top"
              alt="Login Image"
            />
            <div class="card-body">
              <h5 class="card-title">Sign In</h5>
              <p class="card-text">
                Enter your details to login and access awesome shows
              </p>
              <p class="small fw-bold mt-2 pt-1 mb-0">
                Don't have an account?
                <router-link to="/user/sign-up" class="link-danger">Register</router-link>
              </p>
            </div>
          </div>
        </div>
        <div class="col-md-8 col-lg-6 col-xl-4 offset-xl-1 mt-3">
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
