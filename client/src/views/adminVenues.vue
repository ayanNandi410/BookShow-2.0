<script>
import AdminVenueCard from '../components/AdminVenueCard.vue'
import ToastMsg from '../components/toastMsg.vue'
import { fetchCities, fetchVenues, deleteVenue, fetchShowsByVenue, exportVenue } from '../api';

export default {
  name: "adminVenues",
  data() {
    return {
      user : this.$store.getters.fetch_user_details,
      venues: [],
      cities: [],
      showsForVenue: [],
      loading: false,
      showsLoading: false,
      venueChoice: "",
      toastShow: false,
      header: "",
      head_end: "",
      message: "",
      type: "",
    };
  },
  methods: {

    updatCurVenue(name, id) {
      this.$store.commit('set_choosen_venue', { id: id, name: name });
      this.$router.push('/admin/venue/update');
    },

    closeToast() {
      this.toastShow = false;
    },

    load_all_cities(){
      fetchCities()
      .then(async res =>  {
          const data = await res.json()
          console.log(data)
          
          if(!res.ok){
            this.head_end = data.error_code;
            this.message = data.error_message;
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

  fetchVenuesforCity(){
    var e = document.getElementById("cityChoice");
    var city = e.value;
    this.loading = true;

      fetchVenues(this.user.auth_token,city,'admin')
      .then(async res =>  {
          const data = await res.json()
          console.log(data)
          
          if(!res.ok){
            this.head_end = data.error_code;
            this.message = data.error_message;
            this.loading = false;
          }
          else{
            this.venues = data;
            this.loading = false;
          }
          
      })
      .catch(e => {
          context.commit('set_error_message', { error_message: e});
          console.log("Fetch Error: "+e)
          }
      );   
  },

  deleteVenueModal(name,id){
    this.venueChoice = { name: name, id: id }
  },

  deleteChoosenVenue(){
    this.type = "error";
    this.toastShow = true;
    this.header = "Delete Venue";

    deleteVenue(this.user.auth_token,this.venueChoice.id)
      .then(async res =>  {
          const data = await res.json()
          console.log(data)

          if(!res.ok){
            this.head_end = data.error_code;
            this.message = data.error_message;
          }
          else{
            this.message = "Success";
            this.type = "info";
            this.fetchVenuesforCity();
          }
          
      })
      .catch(e => {
        this.message = e.data;
        console.log("Fetch Error: "+e)
          }
      );   
  },

  displayShows(name,id){
    this.venueChoice = { name: name, id: id }
    this.showsLoading = true;
    var canvasBody = document.getElementById("fetchShowsError");

    fetchShowsByVenue(this.user.auth_token,this.venueChoice.id)
      .then(async res =>  {
          const data = await res.json()
          console.log(data)
          this.deleteResult = true;
          this.showsLoading = false;

          if(!res.ok){
            this.error_message = data.error_message;
            this.error_code = data.error_code;
            canvasBody.innerHTML = "API Error: " + data.error_code + " , " + data.error_message;
          }
          else{
            this.showsForVenue = data;
          }
          
      })
      .catch(e => {
        this.showsLoading = false;
        this.error_message = e.data;
        canvasBody.innerHTML = "Fetch Error: " + data.error_code + " , " + data.error_message;
          console.log("Fetch Error: "+e)
          }
      ); 
  },

  showTimings(showDetails){
    const details = {
      showId: showDetails.id,
      showName: showDetails.name,
      venueId: this.venueChoice.id,
      venueName: this.venueChoice.name
    }
    this.$router.push({ path: '/admin/timings/view', query: details })
  },

  exportVenue(name,id){
    exportVenue(this.user.auth_token,id)
      .then(async res =>  {
          const data = await res.json()
          console.log(data)


          if(!res.ok){
            this.error_message = data.error_message;
          }
          else{
            this.$store.commit('set_notif', { message: name })
          }
          
      })
      .catch(e => {
          console.log("Fetch Error: "+e)
          }
      ); 
  }

},
computed: {
    loading(){
        return this.loading;
    },
    showsLoading(){
        return this.showsLoading;
    },
},

components: { AdminVenueCard, ToastMsg },

  beforeMount() {
    this.load_all_cities();
  },

  onMounted(){
    this.$store.commit('set_user_details_from_local');
    this.user = this.$store.getters.fetch_user_details;
  }

};
</script>


<template>
    
<div class="body container" style="min-height: 100%;">

  <ToastMsg 
    v-bind:header="header" 
    v-bind:head_end="head_end" 
    v-bind:message="message" 
    v-bind:type="type" 
    v-if="toastShow"
    @close-toast="closeToast" />

    <!-- Offcanvas for Shows -->
  <div class="offcanvas offcanvas-bottom" tabindex="-1" id="offcanvasShows" data-bs-scroll="true" data-bs-backdrop="false"
    aria-labelledby="offcanvasBottomLabel" style="height: 90%;">

    <div class="offcanvas-header">
      <h5 class="offcanvas-title" id="offcanvasShowsTitle" >Shows for : {{ venueChoice.name }}</h5>
      <button type="button" class="btn-close text-reset" data-bs-dismiss="offcanvas" aria-label="Close"></button>
    </div>
    <div class="offcanvas-body">    
      <div style="margin: auto 50%;">
        <div class="spinner-border spinner-border-lg text-primary" role="status" v-if="showsLoading">
        <span class="visually-hidden">Loading...</span>
      </div>
      </div>
      <h4 class="alert alert-primary text-center" style="margin: 8% 10% 20%;" 
        v-if="showsForVenue.length==0">Did not find any venue. Try later..<br/><br/>
        <p id="fetchShowsError" style="display: none;  background-color: rgb(110, 164, 164); 
        width: fit-content; margin: auto; padding: 2px 10px;" ></p>
      </h4>

      <div class="row row-cols-2 row-cols-sm-5 g-4 mt-4" 
            style="padding: 5px 20px; margin: auto 10px;" id="cardListShows">
          <div class="col" v-for="show in showsForVenue">
            <div class="col">
              <div class="card">
                <div class="card-body">
                  <h5 class="card-title">{{ show.name }}</h5>
                  <br/>
                  <p class="card-text">
                    Duration : {{ show.duration }}
                    <br/>
                    Rating : {{ show.rating }} / 10
                    </p>
                  <a class="btn btn-primary" @click="showTimings({ 
                    name: show.name, id: show.id })">View Timings</a>
                </div>
              </div>
        </div>
          </div>
      </div>
    </div>
  </div>

    <div class="modal fade" id="deleteModal" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
        <div class="modal-header">
            <h1 class="modal-title fs-5" id="exampleModalLabel">Venue Details</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
      <div class="modal-body" id="deleteModalBody">
        <p>Venue: {{ this.venueChoice.name }}</p><br/>
        <p>Are you sure you want to delete venue ?</p>
      </div>
      <div class="modal-footer">
        <p id="deleteResult"></p>
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
        <a href="#" id="venueDeleteBt" class="btn btn-primary" data-bs-dismiss="modal" @click="deleteChoosenVenue">Delete Venue</a>
      </div>
        </div>
    </div>
    </div>


    <div class="row">
      <div class="col-12 col-sm-2">
          <h2 style="display: inline;">Venues in</h2>
    </div>
    <div class="col-12 col-sm-4">
          <div class="input-group mb-3">
            <label class="input-group-text" for="inputGroupSelect01">City</label>
            <select class="form-select" id="cityChoice">
                <option value="0">Choose city</option>
                <option v-for="city in cities" :value="city">{{ city }}</option>
            </select>
            <button class="btn btn-success" @click="fetchVenuesforCity">Search</button>
          </div>
      </div>
      <div class="col-12 col-sm-2 offset-sm-4">
        <router-link to="/admin/venue/add" class="btn btn-info">+ Add Venue</router-link>
      </div>
      <hr/>  
    </div>
    <br/><br/>

    <div style="margin: auto 50%;">
        <div class="spinner-border spinner-border-lg text-primary" role="status" v-if="loading">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <h2 class="alert alert-primary text-center" style="margin: 8% 10% 20%;" v-if="venues.length==0">Did not find any venue. Try again..</h2>

    <div class="row row-cols-md-3 row-cols-sm-1 g-3" v-else>    
        <AdminVenueCard v-for="venue in venues" 
        v-bind:id=venue.id.toString()
        v-bind:name=venue.name 
        v-bind:capacity=venue.capacity 
        v-bind:location=venue.location 
        v-bind:timestamp="venue.timestamp"
        @updateVenue="updatCurVenue"
        @deleteVenue="deleteVenueModal"
        @exportVeueDet="exportVenue"
        @displayShows="displayShows"/>
    </div>
</div>
</template>