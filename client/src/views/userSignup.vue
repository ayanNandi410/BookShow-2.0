<template>
  <div class="body">
    <div class="container-fluid h-custom">
      <div class="row d-flex justify-content-center h-100">
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
        <div class="col-12 col-sm-5 offset-1">
          <form
            class="mt-4"
            action="/userSignup"
            method="post"
            onsubmit="return formValidate();"
          >
            <!-- Name input -->
            <div class="row mb-4">
              <div class="col-12 col-sm-6">
                <div class="form-floating">
                  <input
                    type="text"
                    id="signup_firstname"
                    name="signup_firstname"
                    class="form-control form-control-lg"
                    placeholder="First Name"
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
                    required
                  />
                  <label for="signup_lastname"> Last Name</label>
                </div>
              </div>
            </div>

            <div class="form-floating mb-4 col-12">
              <input
                type="email"
                id="signup_email"
                name="signup_email"
                class="form-control form-control-lg"
                placeholder="Enter a valid email address"
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
                type="submit"
                class="btn btn-success btn-lg"
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
