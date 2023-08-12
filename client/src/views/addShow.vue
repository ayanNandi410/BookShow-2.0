<script>
import ToastMsg from '../components/toastMsg.vue'
import { addShow } from '../api'

export default {
  name: "addShow",
  data() {
    return {
      user : this.$store.getters.fetch_user_details,
      toastShow: false,
      header: "",
      head_end: "",
      message: "",
      type: "",
      name: "",
      showId: null,
      rating: null,
      tags: [],
      languages: [],
      duration: "",
      registered: false,
    };
  },
  methods: {

    saveShow(id,name){
            this.$store.commit('set_choosen_show', { id: id, name: name });
    },

    closeToast(){
      this.toastShow = false;
    },

    allocateShow(){
        if(this.registered){
            this.$store.commit('set_choosen_show', { id: this.showId, name: this.name });
            this.$router.replace('/admin/allocateTimings');
        }
        else{
            this.type = 'info';
            this.toastShow = true;
            this.message = "Register Show First";
            this.header = "Allocate Show";
        }
    },

    formValidate(){
        let result = true;

        let rating = document.getElementById('showRating');
        if((rating.value>10) ||(rating.value<0) || (rating.value != Math.floor(rating.value)))
        {
            document.getElementById('ratingCheck').style.display = "block";
            result = false;
        }
        else{
            document.getElementById('ratingCheck').style.display = "none";
        }


        let tags = document.getElementsByName('tags');
        let count = 0;
        for(var i=0; tags[i]; ++i)
        {
            if(tags[i].checked)
            {
                count++;
                break;
            }
        }
        if(count==0)
        {
            document.getElementById('tagCheck').style.display = "block";
            result = false;
        }
        else{
            document.getElementById('tagCheck').style.display = "none";
        }

        let lngs = document.getElementsByName('languages');
        count = 0;
        for(var i=0; lngs[i]; ++i)
        {
            if(lngs[i].checked)
            {
                count++;
                break;
            }
        }
        if(count==0)
        {
            document.getElementById('langCheck').style.display = "block";
            result = false;
        }
        else{
            document.getElementById('langCheck').style.display = "none";
        }

        if(result)
        {
            this.addNewShow();
        }
        return false;
    },

    addNewShow(){

    this.header = "Add New Show";
    this.type = "error";

    const show = { name: this.name, rating: this.rating, tags: this.tags, languages: this.languages, duration: this.duration }

    addShow(this.user.auth_token,show)
      .then(async res =>  {
          const data = await res.json()
          this.toastShow = true;
          
          if(!res.ok){
            this.head_end = data.error_code;
            this.message = data.error_message;
            
          }
          else{
            this.message = "Success";
            this.showId = data.id;
            this.type = "info";
            this.registered = true;
          }
          
      })
      .catch(e => {
        this.message = e.data;
        console.log("Fetch Error: "+e)
        
    });   
  },

},

  beforeMount() {
  },

  onMounted(){
    this.$store.commit('set_user_details_from_local');
    this.user = this.$store.getters.fetch_user_details;
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

    <div class="container h-custom">
        <div class="row">
        <div class="col-12 col-sm-4">
            <h2>Add new Show</h2>
        </div>
        <div class="col-12 col-sm-2 offset-sm-6">
            <button class="btn btn-success" @click="$router.go(-1)">Go Back</button>
        </div>
    </div>
        <hr/><br/>
      <div class="d-flex justify-content-center align-items-center h-100">

          <form class="mt-4" onsubmit="return false;">  
            <div class="row mb-3">
                <div class="col-12 col-sm-6">
                    <div class="input-group input-group-md mb-3">
                        <span class="input-group-text" name="showName" id="showName">Name</span>
                        <input type="text" class="form-control" name="showName" v-model="name"
                        placeholder="Show Name" aria-label="Show Name" required>
                    </div>
                </div>
                <div class="col-12 col-sm-6 mb-3">
                    <div class="input-group input-group-md">
                        <span class="input-group-text">Initial Rating</span>
                        <input type="text" class="form-control" name="showRating" id="showRating" v-model="rating"
                        placeholder="Out of 10" aria-label="Show Rating" required>
                        <div id="ratingCheck" class="invalid-feedback">&emsp;Invalid value for rating ( Must be 1-5 and a integer )</div>
                    </div>
                </div>
            </div>

            <div class="row mb-3">
                <div class="col-12">
                    <div class="input-group input-group-md">
                        <span class="input-group-text">Tags</span>
                        <div class="form-control">
                            <div class="form-check form-check-inline">
                                <input type="checkbox" class="form-check-input" 
                                id="TagAction" name="tags" value="Action" v-model="tags">
                                <label class="form-check-label" for="Action"> Action</label>
                            </div>
                            <div class="form-check form-check-inline">
                                <input type="checkbox" class="form-check-input" 
                                id="TagThriller" name="tags" value="Thriller" v-model="tags">
                                <label for="Thriller" class="form-check-label"> Thriller</label>
                            </div>
                            <div class="form-check form-check-inline">
                                <input type="checkbox" class="form-check-input" 
                                id="TagComedy" name="tags" value="Comedy" v-model="tags">
                                <label for="Comedy" class="form-check-label"> Comedy</label>    
                            </div>
                            <div class="form-check form-check-inline">
                                <input type="checkbox" class="form-check-input" 
                                id="TagHorror" name="tags" value="Horror" v-model="tags">
                                <label class="form-check-label" for="Horror"> Horror</label>
                            </div>
                            <div class="form-check form-check-inline">
                                <input type="checkbox" class="form-check-input" 
                                id="TagMystery" name="tags" value="Mystery" v-model="tags">
                                <label for="Mystery" class="form-check-label"> Mystery</label>
                            </div>
                            <div class="form-check form-check-inline">
                                <input type="checkbox" class="form-check-input" 
                                id="TagFantasy" name="tags" value="Fantasy" v-model="tags">
                                <label for="Fantasy" class="form-check-label"> Fantasy</label>    
                            </div>
                            <div class="form-check form-check-inline">
                                <input type="checkbox" class="form-check-input" 
                                id="TagDrama" name="tags" value="Drama" v-model="tags">
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
                                <input type="checkbox" class="form-check-input" 
                                id="LangEnglish" name="languages" value="English" v-model="languages">
                                <label class="form-check-label" for="English"> English</label>
                            </div>
                            <div class="form-check form-check-inline">
                                <input type="checkbox" class="form-check-input" 
                                id="LangHindi" name="languages" value="Hindi" v-model="languages">
                                <label for="Hindi" class="form-check-label"> Hindi</label>
                            </div>
                            <div class="form-check form-check-inline">
                                <input type="checkbox" class="form-check-input" 
                                id="LangBengali" name="languages" value="Bengali" v-model="languages">
                                <label for="Bengali" class="form-check-label"> Bengali</label>    
                            </div>
                            <div class="form-check form-check-inline">
                                <input type="checkbox" class="form-check-input" 
                                id="LangTamil" name="languages" value="Tamil" v-model="languages">
                                <label class="form-check-label" for="Tamil"> Tamil</label>
                            </div>
                            <div class="form-check form-check-inline">
                                <input type="checkbox" class="form-check-input" 
                                id="LangTelegu" name="languages" value="Telegu" v-model="languages">
                                <label for="Telegu" class="form-check-label"> Telegu</label>
                            </div>
                            <div class="form-check form-check-inline">
                                <input type="checkbox" class="form-check-input" 
                                id="LangMalayalam" name="languages" value="Malayalam" v-model="languages">
                                <label for="Malayalam" class="form-check-label"> Malayalam</label>    
                            </div>
                        </div>
                    </div>
                </div>
                <div id="langCheck" class="invalid-feedback">&emsp;One Language must be selected</div>
            </div>

            <div class="row mb-3">
                <div class="col-4">
                    <div class="input-group input-group-md mb-3">
                        <span class="input-group-text" >Duration</span>
                        <input type="text" class="form-control" name="showDuration" 
                        id="showDuration" placeholder="2 hrs 3 min" aria-label="Show Duration"  v-model="duration" required>
                    </div>
                </div>
            </div>

            <div class="row mb-3">
                <div class="col-4 offset-2">
                    <button class="btn btn-primary btn-md" @click="formValidate"
                    style="padding-left: 2.5rem; padding-right: 2.5rem;">Register Show</button>
                </div>
                <div class="col-4">
                    <button class="btn btn-success btn-md" @click="allocateShow" 
                    style="padding-left: 2.5rem; padding-right: 2.5rem;" >Allocate to Venues</button>
                </div>
            </div>
  
          </form>
      </div>
    </div>
</div>
</template>