<script>
import { onMounted, onUpdated } from 'vue';
import { fetchCities } from '../api'

export default {
  name: "adminHome",
  data() {
    return {
      user : this.$store.getters.fetch_user_details,
      cities: [],
      error_code: "",
      error_message: "",
    };
  },
  methods: {
    load_all_cities(){
      fetchCities()
      .then(async res =>  {
          const data = await res.json()
          console.log(data)
          
          if(!res.ok){
            this.error_message = data.error_message;
            this.error_code = data.error_code;
          }
          else{
            this.cities = data.cities;
          }
          
      })
      .catch(e => {
          context.commit('set_error_message', { error_message: e});
          console.log("Fetch Error: "+e)
          }
      );   
  },

  routeVenues(city){
    this.$router.push({ path: `/user/venues/forCity/${city}` })
  }
},

  beforeMount() {
    this.load_all_cities();
  },

  onMounted(){
    if(localStorage.auth_token){
      this.auth_token = localStorage.auth_token;
    }
    else{
        this.$router.push('/admin/login');
    }
  },

  computed: {
  }
};
</script>

<template>
    <!--Choose City Modal -->
<div class="modal fade in" tabindex="-1" id="cityModal" data-bs-backdrop="static">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="staticBackdropLabel">Choose City</h5>
        </div>
        <div class="modal-body " >
          <div v-if="cities != []" class="row row-cols-md-3 row-cols-sm-1 g-3">
            <div class="col"  v-for="city in cities">
            <div class="card" style="width: fit-content;">
              <img src="@/assets/city.svg" class="card-img-top mt-3" alt="" height="50" width="50" />
                <div class="card-body">
                  <a href="#" class="btn btn-sm btn-info" data-bs-dismiss="modal" data-bs-target="#cityModal" style="margin: auto 1%;" @click="routeVenues(city)">{{ city }}</a>
                </div>
              </div>
            </div>
          </div>
          <p v-else style="text-align: center;">{{ error_message }}</p>
        </div>
      </div>
    </div>
</div>
<div class="body vh-100 container">
  <div class="jumbotron" style="margin-top: 10%; padding: 5% 10%; background-color: #c7dded;">
    <h1 class="display-4">Welcome <i>{{ user.name }}</i></h1><br/>
    <p class="lead">You have reached a place where you can explore all venues available in your City
        and book your favourite show as well. You may use the links available at the top to begin your journey.</p>
    <hr class="my-4">
    <p></p>
    <p class="lead">
      <!-- <button class="btn btn-primary btn-md" type="button" 
        data-bs-toggle="modal" data-bs-target="#cityModal">See Venues</button>  -->
    </p>
  </div>
</div>
</template>