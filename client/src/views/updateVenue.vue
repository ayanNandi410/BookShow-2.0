<script>
import ToastMsg from '../components/toastMsg.vue'
import { updateVenue } from '../api'

export default {
  name: "updateVenue",
  data() {
    return {
      user : this.$store.getters.fetch_user_details,
      venue: { id: this.$store.state.venue.id, name: this.$store.state.venue.name },
      toastShow: false,
      header: "",
      head_end: "",
      message: "",
      type: "",
      name: "",
      location: "",
      city: "",
      capacity: "",
      desc: "",
    };
  },
  methods: {

    closeToast(){
      this.toastShow = false;
    },

    updateCurVenue(){
    this.header = "Update Venue";
    this.type = "error";

    const CurVenue = { 
        id: this.venue.id,
        name: this.name, 
        location:this.location, 
        city:this.city, 
        capacity:this.capacity, 
        description: this.desc
    }

    updateVenue(this.user.auth_token,CurVenue)
      .then(async res =>  {
          const data = await res.json()
          this.toastShow = true;
          
          if(!res.ok){
            this.head_end = data.error_code;
            this.message = data.error_message;
            
          }
          else{
            this.message = "Success";
            this.type = "info";
          }
          
      })
      .catch(e => {
        this.message = e.data;
        console.log("Fetch Error: "+e)
        
    });   
  },

    formValidate(){
        let result = true;

        let capacity = document.getElementById('venueCapacity');
        
        if(capacity.value < 40)
        {
            document.getElementById('capCheck').style.display = "block";
            result = false;
        }
        else{
            document.getElementById('capCheck').style.display = "none";
        }

        let desc = document.getElementById('venueDescription');
        if(desc.value.length < 40)
        {
            document.getElementById('descCheck').style.display = "block";
            result = false;
        }
        else{
            document.getElementById('descCheck').style.display = "none";
        }

        if(result==false)
        {
            return result;
        }
        else{
            this.updateCurVenue();
        }
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

<div class="container">
    <div class="row">
        <div class="col-12 col-sm-4">
            <h2>Update Venue</h2>
        </div>
        <div class="col-12 col-sm-2 offset-sm-6">
            <button class="btn btn-success" @click="$router.go(-1)">Go Back</button>
        </div>
    </div>
    <hr/><br/>
  <div class="d-flex justify-content-center align-items-center h-100">

      <form class="mt-4" onsubmit="return false;">  
        <!-- Name input -->
        <div class="row mb-3">
            <div class="col-12 col-sm-6">
                <div class="input-group input-group-lg mb-3">
                    <span class="input-group-text" name="venueName">Venue Name</span>
                    <input type="text" class="form-control" name="venueName" id="venueName" 
                    v-model="name"  placeholder="Allen Hall" aria-label="venueName" required>
                </div>
            </div>
            <div class="col-12 col-sm-6">
                <div class="input-group input-group-lg mb-3">
                    <span class="input-group-text">Venue Location</span>
                    <input type="text" class="form-control" name="venueLocation" id="venueLocation" 
                    v-model="location"  placeholder="Beleghata" aria-label="venueLocation" required>
                </div>
            </div>
        </div>
        <div class="col-12 col-sm-6">
            <div class="input-group input-group-lg mb-3">
                <span class="input-group-text">Venue City</span>
                <input type="text" class="form-control" name="venueCity" id="venueCity" 
                v-model="city"  placeholder="Kolkata" aria-label="venueCity" required>
            </div>
        </div>
        <!--
        <div class="row mb-3">
            <div class="input-group input-group-lg">
                <input type="file" class="form-control" id="venueImage" name="venueImage">
                <label class="input-group-text" for="venueImage">Upload Image</label>
              </div>
        </div>
        -->
        <div class="row mb-3">
            <div class="col-4">
                <div class="input-group input-group-lg mb-3">
                    <span class="input-group-text" >Venue Capacity</span>
                    <input type="number" class="form-control" name="venueCapacity" id="venueCapacity" 
                    v-model="capacity"  placeholder="450" aria-label="venueCapacity" required>
                    <div id="capCheck" class="invalid-feedback">&emsp;Capacity of Venue too less</div>
                </div>
            </div>
        </div>

        <div class="row mb-3">
            <div class="input-group input-group-lg mb-3">
                <span class="input-group-text">Venue Description</span>
                <textarea class="form-control" name="venueDescription" id="venueDescription" 
                aria-label="With textarea" v-model="desc" placeholder="At least 50 characters" required></textarea>
                <div id="descCheck" class="invalid-feedback">&emsp;At least 50 characters are necessary</div>
            </div>
        </div>

        <div class="row mb-3">
            <div class="col-4 offset-5">
                <button class="btn btn-primary btn-lg" @click="formValidate"
                style="padding-left: 2.5rem; padding-right: 2.5rem;">Update Venue</button>
            </div>
        </div>

      </form>
  </div>
</div>
</div>
</template>