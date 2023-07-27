<template>
  <div class="body">
    <div class="container-fluid">
      <div class="row d-flex justify-content-center">
        <div class="col-md-9 col-lg-6 col-xl-5">
          <div class="card" style="width: 25rem">
            <img
              src="@/assets/admin.jpg"
              class="card-img-top"
              alt="Sample image"
              width="200"
              height="400"
            />
            <div class="card-body" style="background-color: rgb(204, 235, 247)">
              <h5 class="card-title">Sign In</h5>
              <p class="card-text">Administrator Login</p>
            </div>
          </div>
        </div>
        <div class="col-md-8 col-lg-6 col-xl-4 offset-xl-1">
          <form class="mt-4" action="/adminLogin" method="post">
            <h3 class="alert alert-primary mb-4"> Enter Details</h3>
            <!-- Email input -->
            <div class="form-floating mb-4">
              <input
                type="email"
                id="login_email"
                name="login_email"
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
                class="form-control form-control-lg"
                placeholder="Enter password"
              />
              <label class="form-label" for="form3Example4">Password</label>
            </div>

            <div class="row">
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
                type="submit"
                class="btn btn-success btn-lg"
                style="padding-left: 2.5rem; padding-right: 2.5rem"
              >
                Login
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
