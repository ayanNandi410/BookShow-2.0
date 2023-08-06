<script>
import ToastMsg from '../components/toastMsg.vue'
import { register_user, user_addRole } from '../api';
import { onMounted } from 'vue';

export default {
  name: "UserLogin",
  data() {
    return {
      auth_token: "",
      first_name: "",
      last_name: "",
      username: "",
      email: "",
      password: "",
      rep_password: "",
      header: "",
      head_end: "",
      message: "",
      type: "",
      toastShow: false,
    };
  },
  methods: {
    isValidEmail() {
      return /^[^@]+@\w+(\.\w+)+\w$/.test(this.email);
    },

    closeToast() {
      this.toastShow = false;
    },

    addUserRole(){
      user_addRole(this.email)
          .then(async res => {
            const data = await res.data

            if (!res.ok) {
              this.type = "error"
              this.message = data;
              this.header = "Validation Error";
            }
            else {
              this.type = "info";
              this.header = "User Registration"
              this.message = "Proceed to login...";
            }

          })
          .catch(e => {
            this.type = "error"
            this.message = e.message;
            this.header = "Fetch Error"
          }
          );
    },

    submitForm() {
      this.type = "info";
      this.toastShow = true;

      if (!this.isValidEmail()) {
        console.log("Invalid email");
        this.type = "error";
        this.message = "Invalid email";
        this.header = "Form Error";
      }
      else if (this.password.length < 8) {
        console.log("Password Length too short");
        this.type = "error";
        this.message = "Password Length too short";
        this.header = "Form Error";
      }
      else if(this.password != this.rep_password) {
        document.getElementById('passwdCheck').style.display = "block";
      }
      else {
        document.getElementById('passwdCheck').style.display = "none";

        register_user(
          {
            first_name: this.first_name,
            last_name: this.last_name,
            username: this.username,
            email: this.email,
            password: this.password,
          })
          .then(async res => {
            const data = await res.json()

            if (!res.ok) {
              this.type = "error"
              this.message = data.response.errors[0];
              this.header = "Validation Error";
            }
            else {
              this.type = "info";
              this.header = "User Registration"
              this.message = "Registered successfully...";
              this.addUserRole();
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
  <div class="body">
      
      <ToastMsg 
      v-bind:header="header" 
      v-bind:head_end="head_end" 
      v-bind:message="message" 
      v-bind:type="type" 
      v-if="toastShow"
      @close-toast="closeToast" />

    <div class="container-fluid h-custom">
      <div class="row d-flex justify-content-center h-100 g-2">
        <div class="col-12 col-sm-4">
          <div class="row">
            <h3 class="alert alert-warning mb-4">Sign Up to book shows!</h3>
          </div>
          <div class="row">
            <img
              src="@/assets/signup.png"
              width="250"
              height="420"
            />
          </div>
        </div>
        <div class="col-12 col-sm-5 offset-1 mt-4">
          <form
            onsubmit="return false;"
          >
            <!-- Name input -->
            <div class="row mb-4">
              <div class="col-12 col-sm-6 mb-2">
                <div class="form-floating">
                  <input
                    type="text"
                    id="signup_firstname"
                    name="signup_firstname"
                    class="form-control form-control-lg"
                    placeholder="First Name"
                    v-model="first_name"
                    required
                  />
                  <label for="signup_firstname"> First Name</label>
                </div>
              </div>

              <div class="col-12 col-sm-6">
                <div class="form-floating">
                  <input
                    type="text"
                    id="signup_lastname"
                    name="signup_lastname"
                    class="form-control form-control-lg"
                    placeholder="Last Name"
                    v-model="last_name"
                    required
                  />
                  <label for="signup_lastname"> Last Name</label>
                </div>
              </div>
            </div>

              <div class="form-floating mb-4 col-12">
                <input
                  type="text"
                  id="signup_username"
                  name="signup_username"
                  class="form-control form-control-lg"
                  placeholder="Enter a valid username"
                  v-model="username"
                  required
                />
                <label class="form-label" for="signup_email">Username</label>
              </div>

            <div class="form-floating mb-4 col-12">
              <input
                type="email"
                id="signup_email"
                name="signup_email"
                class="form-control form-control-lg"
                placeholder="Enter a valid email address"
                v-model="email"
                required
              />
              <label class="form-label" for="signup_email">Email address</label>
            </div>

            <!-- Password input -->
            <div class="form-floating mb-3 col-12">
              <input
                type="password"
                id="signup_passwd"
                name="signup_passwd"
                class="form-control form-control-lg"
                placeholder="Enter password"
                minlength="6"
                v-model="password"
                required
              />
              <label class="form-label" for="signup_passwd">Password</label>
            </div>

            <!-- Reenter Password input -->
            <div class="form-floating mb-3 col-12">
              <input
                type="password"
                id="signup_check_passwd"
                name="signup_check_passwd"
                class="form-control form-control-lg"
                placeholder="Retype password"
                minlength="6"
                v-model="rep_password"
                required
              />
              <label class="form-label" for="signup_check_passwd"
                >Retype Password</label
              >
              <div id="passwdCheck" class="invalid-feedback">
                &emsp;Passwords do not match
              </div>
            </div>

            <div class="text-lg-start mt-4 pt-2">
              <button
                class="btn btn-success btn-lg"
                @click="submitForm"
                style="padding-left: 2.5rem; padding-right: 2.5rem"
              >
                Register
              </button>
              <p class="small fw-bold mt-2 pt-1 mb-0">
                Already have an account?
                <a href="/userLogin" class="link-danger">Login</a>
              </p>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>
