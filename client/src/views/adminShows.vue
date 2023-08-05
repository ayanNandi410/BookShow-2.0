<script>
import AdminShowCard from '../components/AdminShowCard.vue'
import { fetchPopularShows, deleteShow, fetchShowsByName } from '../api';
import ToastMsg from '../components/toastMsg.vue'

export default {
  name: "adminShows",
  data() {
    return {
      user : this.$store.getters.fetch_user_details,
      shows: [],
      loading: false,
      showChoice: {},
      name: "",
      rating: "",
      duration: "",
      timestamp: "",
      tags: [],
      languages: [],
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

    closeToast() {
      this.toastShow = false;
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

  deleteShowModal(name,id){
    this.showChoice = { name: name, id: id }
  },

  deleteChoosenShow(){
    this.type = "error";
    this.toastShow = true;
    this.header = "Delete Show";

    deleteShow(this.user.auth_token,this.showChoice.id)
      .then(async res =>  {
          const data = await res.json()
          console.log(data)
          this.deleteResult = true;

          if(!res.ok){
            this.head_end = data.error_code;
            this.message = data.error_message;
          }
          else{
            this.message = "Success";
            this.type = "info";
            this.fetchPopShows();
          }
          
      })
      .catch(e => {
        this.message = e.data;
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

components: { AdminShowCard, ToastMsg },

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

    <div class="modal fade" id="deleteModal" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
        <div class="modal-header">
            <h1 class="modal-title fs-5" id="exampleModalLabel">Show Details</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
      <div class="modal-body" id="deleteModalBody">
        <p>Show : {{ this.showChoice.name }}</p><br/>
        <p>Are you sure you want to delete show ?</p>
      </div>
      <div class="modal-footer">
        <p id="deleteResult"></p>
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
        <a href="#" id="showDeleteBt" class="btn btn-primary" data-bs-dismiss="modal" @click="deleteChoosenShow">Delete Show</a>
      </div>
        </div>
    </div>
    </div>

    <div class="row">
      <div class="col-12 col-sm-5" v-if="!searched"><h2>&emsp;Latest Shows (Top 20)</h2></div>
      <div class="col-12 col-sm-5" v-else><h2>&emsp;Search Results</h2></div>
      <div class="col-12 col-sm-4">
          <div class="input-group mb-3">
              <label class="input-group-text" for="inputGroupSelect01">Show Name</label>
              <input class="form-control form-control-sm" name="searchShowName" type="search" 
              placeholder="Search for shows" aria-label="Search" v-model="showName">
              <button class="btn btn-success" @click="load_shows_by_name">Search</button>
          </div>
      </div>
      <div class="col-12 col-sm-2 offset-sm-1">
        <router-link to="/admin/show/add" class="btn btn-info">+ Add Show</router-link>
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
      <AdminShowCard v-for="show in shows" 
        v-bind:id=show.id.toString()
        v-bind:name="show.name"
        v-bind:duration="show.duration"
        v-bind:rating="show.rating"
        v-bind:tags="show.tags"
        v-bind:languages="show.languages"
        v-bind:timestamp="show.timestamp"
        @deleteShow="deleteShowModal"/>
    </div>
</div>
</template>