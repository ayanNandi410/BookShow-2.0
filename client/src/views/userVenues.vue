<script>
import VenueCard from '../components/UserVenueCard.vue'
import { fetchVenues } from '../api';

export default {
  name: "userVenues",
  data() {
    return {
      user: this.$store.getters.fetch_user_details,
      venues: [],
      city: this.$route.params.city,
    };
  },
  methods: {
    load_all_venues(city){
      fetchVenues(this.user.auth_token,city, 'user')
      .then(async res =>  {
          const data = await res.json()
          console.log(data)
          
          if(!res.ok){
            this.error_message = data.error_message;
            this.error_code = data.error_code;
          }
          else{
            this.venues = data;
          }
          
      })
      .catch(e => {
        this.error_message = e.data;
          console.log("Fetch Error: "+e)
          }
      );   
  },

},
components: { VenueCard },

  beforeMount() {
    this.load_all_venues(this.city);
  },

  onMounted() {
    this.$store.commit('set_user_details_from_local');
    this.user = this.$store.getters.fetch_user_details;
  },

};
</script>


<template>
    
<div class="body container" style="margin-bottom: 20%;">
    <div class="row">
      <div class="col-12 col-sm-4">
          <h2>Venues in <span class="badge bg-success">{{ city }}</span></h2>
      </div>
      <div class="col-12 col-sm-2 offset-sm-6">
        <button class="btn btn-success" @click="$router.go(-1)">Go Back</button>
      </div>
      <hr/>  
    </div>
    <br/><br/>

    <h2 class="alert alert-primary text-center" v-if="venues == []">No venue available</h2>

    <div class="row row-cols-md-3 row-cols-sm-1 g-3" v-else>    
        <VenueCard v-for="venue in venues" 
        v-bind:id=venue.id.toString()
        v-bind:name=venue.name 
        v-bind:capacity=venue.capacity 
        v-bind:location=venue.location />
    </div>
</div>
</template>