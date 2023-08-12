<script>
import UserShowCard from '../components/UserShowCard.vue'
import { fetchPopularShows, fetchShowsByName, fetchCities, fetchVenuesByShow, fetchReviews, filterShows } from '../api';
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
      filterMd: {
        rating: null,
        tags: [],
        languages: [],
        runningShows: "",
      },
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

    getReviews(id,name){
      fetchReviews(this.user.auth_token,id)
      .then(async res =>  {
          const data = await res.json()
          console.log(data)
          
          if(!res.ok){
            this.head_end = data.error_code;
            this.message = data.error_message;
            this.venuesForShow = [];
          }
          else{
            this.reviews = data;
          }
          
      })
      .catch(e => {
          this.message = e.data;
          console.log("Fetch Error: "+e)
          }
      );   
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
  },

  filterCurShows(){
    this.type = "error";
    this.toastShow = true;
    this.header = "Filter Show";
    this.loading = true;

    const details = {
      runningShows: this.filterMd.runningShows,
      tags: this.filterMd.tags,
      languages: this.filterMd.languages,
      rating: this.filterMd.rating,
    }

    filterShows(this.user.auth_token,details)
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

components: { UserShowCard , ToastMsg },

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


    <!-- Filter Modal -->
    <div class="modal fade" id="filterModal" data-bs-backdrop="static"
    data-bs-keyboard="false" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
            <h1 class="modal-title fs-5" id="filterModalLabel">Filter Shows</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <form onsubmit="return false;">

            <div class="modal-body" id="filterModalBody">
            <div class="container">

                <div class="row mb-3">
                <div class="col-12">
                    <div class="input-group input-group-md">
                        <span class="input-group-text">Tags</span>
                        <div class="form-control">
                            <div class="form-check form-check-inline">
                                <input type="checkbox" class="form-check-input" v-model="filterMd.tags"
                                id="TagAction" name="tags" value="Action">
                                <label class="form-check-label" for="Action"> Action</label>
                            </div>
                            <div class="form-check form-check-inline">
                                <input type="checkbox" class="form-check-input" v-model="filterMd.tags"
                                id="TagThriller" name="tags" value="Thriller">
                                <label for="Thriller" class="form-check-label"> Thriller</label>
                            </div>
                            <div class="form-check form-check-inline">
                                <input type="checkbox" class="form-check-input" v-model="filterMd.tags"
                                id="TagComedy" name="tags" value="Comedy">
                                <label for="Comedy" class="form-check-label"> Comedy</label>    
                            </div>
                            <div class="form-check form-check-inline">
                                <input type="checkbox" class="form-check-input" v-model="filterMd.tags"
                                id="TagHorror" name="tags" value="Horror">
                                <label class="form-check-label" for="Horror"> Horror</label>
                            </div>
                            <div class="form-check form-check-inline">
                                <input type="checkbox" class="form-check-input" v-model="filterMd.tags"
                                id="TagMystery" name="tags" value="Mystery">
                                <label for="Mystery" class="form-check-label"> Mystery</label>
                            </div>
                            <div class="form-check form-check-inline">
                                <input type="checkbox" class="form-check-input" v-model="filterMd.tags"
                                id="TagFantasy" name="tags" value="Fantasy">
                                <label for="Fantasy" class="form-check-label"> Fantasy</label>    
                            </div>
                            <div class="form-check form-check-inline">
                                <input type="checkbox" class="form-check-input" v-model="filterMd.tags"
                                id="TagDrama" name="tags" value="Drama">
                                <label for="Drama" class="form-check-label"> Drama</label>    
                            </div>
                        </div>
                    </div>
                </div>
                <div id="tagCheck" class="invalid-feedback">&emsp;One tag must be selected</div>
                </div>

                <div class="row mb-3">
                <div class="col-12">
                    <div class="input-group input-group-md">
                        <span class="input-group-text">Languages</span>
                        <div class="form-control">
                            <div class="form-check form-check-inline">
                                <input type="checkbox" class="form-check-input" v-model="filterMd.languages"
                                id="LangEnglish" name="languages" value="English">
                                <label class="form-check-label" for="English"> English</label>
                            </div>
                            <div class="form-check form-check-inline">
                                <input type="checkbox" class="form-check-input" v-model="filterMd.languages" 
                                id="LangHindi" name="languages" value="Hindi">
                                <label for="Hindi" class="form-check-label"> Hindi</label>
                            </div>
                            <div class="form-check form-check-inline">
                                <input type="checkbox" class="form-check-input" v-model="filterMd.languages" 
                                id="LangBengali" name="languages" value="Bengali">
                                <label for="Bengali" class="form-check-label"> Bengali</label>    
                            </div>
                            <div class="form-check form-check-inline">
                                <input type="checkbox" class="form-check-input" v-model="filterMd.languages" 
                                id="LangTamil" name="languages" value="Tamil">
                                <label class="form-check-label" for="Tamil"> Tamil</label>
                            </div>
                            <div class="form-check form-check-inline">
                                <input type="checkbox" class="form-check-input" v-model="filterMd.languages" 
                                id="LangTelegu" name="languages" value="Telegu">
                                <label for="Telegu" class="form-check-label"> Telegu</label>
                            </div>
                            <div class="form-check form-check-inline">
                                <input type="checkbox" class="form-check-input" v-model="filterMd.languages" 
                                id="LangMalayalam" name="languages" value="Malayalam">
                                <label for="Malayalam" class="form-check-label"> Malayalam</label>    
                            </div>
                        </div>
                    </div>
                </div>
                <div id="langCheck" class="invalid-feedback">&emsp;One Language must be selected</div>
            </div>

            <div class="col-12 col-sm-8 mb-3">
                <label for="userRating" class="form-label">Rating (greater than) <span id="ratingValue" class="badge bg-primary text-white" on="changeColour();">5</span></label>
                <input type="range" class="form-range" min="0" max="10" step="1" v-model="filterMd.rating"
                name="userRating" id="userRating" onchange="updateRating(this.value);" required>
            </div>
            
            <div class="col-12 mb-3">
                <label for="runningShows" class="form-radio-label">Display only running shows? &emsp14;</label>
                <input type="radio" class="form-radio-input" name="runShows" value="yes" v-model="filterMd.runningShows" checked> Yes
                &emsp14;<input type="radio" class="form-radio-input" name="runShows" v-model="filterMd.runningShows" value="no"> No
            </div>
            <br/>

            </div>
            </div>
            <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            <button id="filterBt" class="btn btn-primary" @click="filterCurShows">Filter</button>
            </div>
            </form>
        </div>
        </div>
    </div>


        <!-- Reviews Modal -->
    <div class="modal fade" id="reviewsModal" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-scrollable">
        <div class="modal-content">
        <div class="modal-header">
            <h1 class="modal-title fs-5" id="reviewsModalLabel">Reviews</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body" id="reviewsModalBody">
            <div  v-if="reviews.length==0">
              <h2 class=" badge bg-warning text-dark">No reviews yet</h2>
            </div>
            <ul class="list-group" id="reviews">
                <li class="list-group-item justify-content-between align-items-start mt-3" v-for="review in reviews">
                <div class="ms-2 me-auto">
                  <div class="fw-bold">{{ review.name }}</div>
                      <p>{{ review.comment }}</p>
                      <img
                        src="@/assets/star-full.svg"
                        class="filter-orange" width="20"
                        v-for="(n, index) in parseInt(review.gRating/2)"
                    />
                    <img
                        src="@/assets/star-empty.svg"
                        class="filter-orange" width="20"
                        v-for="(n, index) in 5 - parseInt(review.gRating/2)"
                    />
                </div>
                <br/><p class="text-muted">By {{ review.user_email }}, on {{ review.timestamp.substring(4,16)}}</p>
                </li>
            </ul>
        </div>
        <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
        </div>
        </div>
    </div>
    </div>

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