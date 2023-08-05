<script>
import UserShowCard from '../components/UserShowCard.vue'
import FilterModal from '../components/filterModal.vue'
import { fetchPopularShows, deleteShow, fetchShowsByName, fetchCities, fetchVenuesByShow } from '../api';
import ToastMsg from '../components/toastMsg.vue'

export default {
  name: "userShows",
  data() {
    return {
      user : this.$store.getters.fetch_user_details,
      shows: [],
      cities: [],
      venuesForShow: [],
      reviews: [],
      showChoice: {},
      loading: false,
      showChoice: {},
      toastShow: false,
      header: "",
      head_end: "",
      message: "",
      type: "",
      searched: false,
      showName: '',
    };
  },
  methods: {

    reloadPage(){
        this.fetchPopShows();
        this.searched = false;
    },

    closeToast() {
      this.toastShow = false;
    },

    saveVenueWithShow(id,name){
            this.$store.commit('set_choosen_show', { id: this.showChoice.id, name: this.showChoice.name });
            this.$store.commit('set_choosen_venue', { id: id, name: name });
        },

    setShow(id,name){
        this.load_all_cities();
        this.showChoice = {
            id: id,
            name: name,
        };
    },

    getVenuesForShow(city){
        fetchVenuesByShow(this.user.auth_token,this.showChoice.id,city)
      .then(async res =>  {
          const data = await res.json()
          console.log(data)
          
          if(!res.ok){
            this.head_end = data.error_code;
            this.message = data.error_message;
            this.venuesForShow = [];
          }
          else{
            this.venuesForShow = data;
          }
          
      })
      .catch(e => {
            this.venuesForShow = [];
          console.log("Fetch Error: "+e)
          }
      );   
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


  fetchPopShows(){
    this.loading = true;

      fetchPopularShows(this.user.auth_token)
      .then(async res =>  {
          const data = await res.json()
          console.log(data)
          
          if(!res.ok){
            this.error_message = data.error_message;
            this.error_code = data.error_code;
            this.loading = false;
          }
          else{
            this.shows = data;
            this.loading = false;
          }
          
      })
      .catch(e => {
        this.error_message = e.data;
          console.log("Fetch Error: "+e)
          }
      );   
  },

  load_shows_by_name(){
    this.type = "error";
    this.toastShow = true;
    this.header = "Search Show";
    this.loading = true;

    fetchShowsByName(this.user.auth_token,this.showName)
      .then(async res =>  {
          const data = await res.json()
          console.log(data)

          if(!res.ok){
            this.head_end = data.error_code;
            this.message = data.error_message;
            this.loading = false;
          }
          else{
            this.toastShow = false;
            this.shows = data;
            this.searched = true;
            this.loading = false;
          }
          
      })
      .catch(e => {
        this.message = e.data;
          console.log("Fetch Error: "+e)
          }
      ); 
  }
},

computed: {
    loading(){
        return this.loading;
    },
},

components: { UserShowCard , ToastMsg, FilterModal },

  beforeMount() {
    this.fetchPopShows();
  },

  onMounted(){
    this.$store.commit('set_user_details_from_local');
    this.user = this.$store.getters.fetch_user_details;
  }

};
</script>


<template>
    <div class="container body">

    <ToastMsg 
    v-bind:header="header" 
    v-bind:head_end="head_end" 
    v-bind:message="message" 
    v-bind:type="type" 
    v-if="toastShow"
    @close-toast="closeToast" />


        <!-- Reviews Modal -->
    <div class="modal fade" id="reviewsModal" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-scrollable">
        <div class="modal-content">
        <div class="modal-header">
            <h1 class="modal-title fs-5" id="reviewsModalLabel">Reviews</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body" id="reviewsModalBody">
            <ul class="list-group" id="reviews">
            </ul>
        </div>
        <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
        </div>
        </div>
    </div>
    </div>

    <FilterModal />

    <div class="offcanvas offcanvas-bottom" tabindex="-1" id="chVenueCanvas" aria-labelledby="offcanvasBottomLabel" 
        style="min-height: 90%;">
        <div class="offcanvas-header">
        <h5 class="offcanvas-title" id="venuesShowTitle">Venues for : {{ showChoice.name }}</h5>
        <button type="button" class="btn-close text-reset" data-bs-dismiss="offcanvas" aria-label="Close"></button>
        </div>
        <div class="offcanvas-body">
            <div id="searchBar">
            <div class="row">
                <div class="col-4">

                    <div class="btn-group dropup">
                        <button type="button" class="btn btn-secondary">
                            Choose City
                        </button>
                        <button type="button" class="btn btn-secondary dropdown-toggle dropdown-toggle-split" data-bs-toggle="dropdown" aria-expanded="false">
                            <span class="visually-hidden">Toggle Dropdown</span>
                        </button>
                        <ul class="dropdown-menu">
                            <li class="dropdown-item" @click="getVenuesForShow(city)" v-for="city in cities">{{ city }}</li>
                        </ul>
                    </div>

                </div>       
            </div>
            <br/><br/>
            </div>
            <h4 class="alert alert-primary text-center m-5" v-if="venuesForShow.length==0">No venues available</h4>
            <div class="row row-cols-2 row-cols-sm-5 row-md-4 g-4" id="chooseVenueCards" v-else>
                <div class="col" v-for="venue in venuesForShow">
                    <div class="card">
                        <div class="card-body">
                        <h5 class="card-title">{{ venue.name }}</h5>
                        <p class="card-text">
                            <br/>Location : &nbsp;{{ venue.location }}, {{ venue.city }} 
                            </p>
                        <router-link to="/user/buyTicket" @click="saveVenueWithShow(venue.id,venue.name)" >
                            <button data-bs-dismiss="offcanvas" class="btn btn-primary">Choose Venue</button></router-link>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="row">
      <div class="col-12 col-sm-4" v-if="!searched"><h2>&emsp;Latest Shows</h2></div>
      <div class="col-12 col-sm-4" v-else><h2>&emsp;Search Results</h2></div>
      <div class="col-12 col-sm-5">
          <div class="input-group mb-3">
              <label class="input-group-text" for="inputGroupSelect01">Show Name</label>
              <input class="form-control form-control-sm" name="searchShowName" type="search" 
              placeholder="Search for shows" aria-label="Search" v-model="showName">
              <button class="btn btn-primary" @click="load_shows_by_name">Search</button>
          </div>
      </div>
      <div class="col-12 col-sm-3">
        <button class="btn btn-success me-2" data-bs-toggle="modal" data-bs-target="#filterModal">Filter Shows</button>
        <button class="btn btn-danger" @click="reloadPage">Clear Filters</button>
      </div>
    </div>
    
    <hr/><br/><br/>

    <div style="margin: auto 50%;">
        <div class="spinner-border spinner-border-lg text-primary" role="status" v-if="loading">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <h2 class="alert alert-primary text-center" style="margin: 8% 10% 20%;" v-if="shows.length==0">Did not find any show. Try again..</h2>

    <div class="row row-cols-md-3 row-cols-sm-2 row-cols-xs-1 row-cols-1 g-3" v-else>    
      <UserShowCard v-for="show in shows" 
        v-bind:id=show.id.toString()
        v-bind:name="show.name"
        v-bind:duration="show.duration"
        v-bind:rating="show.rating"
        v-bind:tags="show.tags"
        v-bind:languages="show.languages"
        v-bind:timestamp="show.timestamp"
        @showReviews="getReviews(show.id,show.name)"
        @showVenues="setShow(show.id,show.name)"
        />
    </div>
</div>
</template>