<script>
import AdminShowCard from '../components/AdminShowCard.vue'
import { fetchPopularShows } from '../api';

export default {
  name: "adminShows",
  data() {
    return {
      shows: [],
      loading: false,
      showChoice: "",
      deleteResult: false,
      name: "",
      rating: "",
      duration: "",
      timestamp: "",
      tags: [],
      languages: [],
    };
  },
  methods: {

  fetchPopShows(){
    this.loading = true;

      fetchPopularShows()
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
    this.ShowChoice = { name: this.name, id: this.id }
  },

  deleteChoosenShow(){
    var delRes = document.getElementById("deleteResult");

    deleteVenue(this.venueChoice.id)
      .then(async res =>  {
          const data = await res.json()
          console.log(data)
          this.deleteResult = true;

          if(!res.ok){
            this.error_message = data.error_message;
            this.error_code = data.error_code;
            delRes.innerHTML = data.error_code + " , " + data.error_message;
          }
          else{
            this.fetchPopShows();
            delRes.innerHTML = "Success."
          }
          
      })
      .catch(e => {
        this.error_message = e.data;
        delRes.innerHTML = data.error_code + " , " + data.error_message;
          console.log("Fetch Error: "+e)
          }
      );   
  }
},

computed: {
    loading(){
        return this.loading;
    },
    deleteRes(){
        return this.deleteResult;
    }
},

components: { AdminShowCard },

  beforeMount() {
    this.fetchPopShows();
  }

};
</script>


<template>
    <div class="container body">
    <div class="row">
      <div class="col-12 col-sm-6"><h2>&emsp;Latest Shows (Top 20)</h2></div>
      <div class="col-12 col-sm-2 offset-sm-4">
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

    <div class="row row-cols-md-3 row-cols-sm-2 row-cols-xs-1 row-cols-1 g-3">    
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