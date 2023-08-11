<script>
import ToastMsg from '../components/toastMsg.vue'
import { fetchTimeslots, registerBooking } from '../api'

export default {
  name: "userTimeslots",
  data() {
    return {
        user : this.$store.getters.fetch_user_details,
        showName: this.$store.state.show.name,
        venueName: this.$store.state.venue.name,
        showId: this.$store.state.show.id,
        venueId: this.$store.state.venue.id,
        timeslots: {},
        bookEntry: {},
        aid: null,
        noTimeslots: false,
        seats: 1,
        avSeats: 0,
        price: 0.00,
        message: "",
        header: "",
        head_end: "",
        type: "",
        toastShow: false,

    };
  },
  methods: {

    confirmBooking(){

      this.toastShow = true;

      const details = {
        vid: this.venueId,
        sid: this.showId,
        aid: this.aid,
        email: this.user.email,
        allocSeats: this.seats,
        totPrice: this.getPrice,
      }

      registerBooking(this.user.auth_token,details)
        .then(async res => {
          const data = await res.json()
          this.header = "Book Ticket";
          this.type = "error";

          if (!res.ok) {
            this.message = data.error_message;
            this.head_end = data.error_code;
            this.loading = false;

          }
          else {
            this.loading = false;
            this.$router.replace('/user/bookings');
          }

        })
        .catch(e => {
          this.message = e.data;
          console.log("Fetch Error: " + e)
        });
    },

    setModalBody(entry, dateIndex){
      this.bookEntry = {
        time: entry.time,
        date: this.timeslots.days[dateIndex].substring(0,16),
        seats_avl: entry.avSeats,
        perPsnPrice: entry.price
      }
      this.price = entry.price;
      this.aid = entry.id;
    },

    fetchAllTimeslots() {
      this.loading = true;
      console.log("inside fetch booking");

      fetchTimeslots(this.user.auth_token,{ sid: this.showId, vid: this.venueId })
        .then(async res => {
          const data = await res.json()
          this.header = "Get Timeslots"

          if (!res.ok) {
            this.message = data.error_message;
            this.head_end = data.error_code;
            this.loading = false;
            this.noTimeslots = true;
          }
          else {
            this.timeslots = data;
            console.log(this.timeslots);
            console.log(this.timeslots.days);
            this.loading = false;
          }

        })
        .catch(e => {
          this.message = e.data;
          console.log("Fetch Error: " + e)
        });
    },
  },
  computed: {
    getPrice(){
      return (this.seats * this.price).toFixed(2);
    }
  },
  components: { ToastMsg },

  beforeMount(){
    this.fetchAllTimeslots();
  },

  onMounted(){
    this.$store.commit('set_user_details_from_local');
    this.user = this.$store.getters.fetch_user_details;
  },

};
</script>

<template>

<ToastMsg 
    v-bind:header="header" 
    v-bind:head_end="head_end" 
    v-bind:message="message" 
    v-bind:type="type" 
    v-if="toastShow"
    @close-toast="closeToast" />

    <!-- Ticket Price Modal -->
<div class="modal fade" id="priceModal" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h1 class="modal-title fs-5" id="priceModalTitle">Slot Details</h1>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body" id="priceModalBody">
        <p>Time: {{ bookEntry.time }}<br/>
        Date: {{ bookEntry.date }}</p>
        <p>Price per seat: <span style="color: red;">&#8377; {{ bookEntry.perPsnPrice }}</span><br/>
        Seats left: {{ bookEntry.seats_avl }}</p>
        <p>Do you want to buy tickets??</p>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
        <router-link to="/user/confirmTicket" data-bs-toggle="modal" data-bs-target="#confirmModal" class="btn btn-primary">Book Tickets</router-link>
      </div>
    </div>
  </div>
</div>

    <!-- Confirm Ticket Modal -->
    <div class="modal fade" id="confirmModal" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h1 class="modal-title fs-5" id="confirmModalTitle">Slot Details</h1>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body" id="confirmModalBody">
        <p>Show : {{ showName }}<br/>Venue : {{ venueName }}</p>
        <p>Time: {{ bookEntry.time }}<br/>
        Date: {{ bookEntry.date }}</p>
        <p>Price per seat: <span style="color: red;">&#8377; {{ bookEntry.perPsnPrice }}</span><br/></p>
        <p>
          <div class="input-group input-group-md mb-3">
            <span class="input-group-text" >Seats</span>
            <input type="number" class="form-control" name="showSeats" 
            id="showSeats" placeholder="Enter value"  v-model="seats" required>
            <div id="seatsCheck" v-if="seats<=0" style="display: block;" class="invalid-feedback">&emsp;Atleast one seat must be booked</div>
          </div>
        </p>
        <p>
          <div class="input-group input-group-md mb-3">
            <span class="input-group-text" >Total Price</span>
            <input type="number" class="form-control" name="showTotPrice" readonly
            id="showTotPrice"  v-model="getPrice" required>
          </div>
        </p>
        <p>Confirm Booking?</p>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
        <button @click="confirmBooking" data-bs-toggle="modal" id="confirmBt" class="btn btn-primary">Confirm</button>
      </div>
    </div>
  </div>
</div>

<div class="body container" style="margin-top: 6%; padding-bottom: 25%;">
  <div class="row text-center">
    <h4 class="alert alert-success mt-3 mb-4">Choose your timeslot</h4><br/>
  </div>
    <div class="row text-center">
      <div class="col-12 col-sm-6">
        <h5 class="alert alert-success">Show: {{ showName }}</h5>
      </div>
      <div class="col-12 col-sm-6">
        <h5 class="alert alert-success">Venue: {{ venueName }}</h5>
      </div>
    </div><hr/>

      <br/><br/><h4 class="alert alert-success text-center" v-if="noTimeslots">No slots Available in this week.<br/> Will be added soon..</h4>

    <div class="card text-center" style="width: fit-content; margin: auto;" v-else>
        <div class="card-header" style="background-color: #1f87c8;">
          <p class="card-text text-white">Choose day by clicking on Date tab from below</p>
          <ul class="nav nav-tabs card-header-tabs" id="timeNavbar">
            <li class="nav-item" v-for="(day,index) in timeslots.days">

              <a class="nav-link text-white" data-bs-toggle="collapse" :href="'#'+index.toString()" v-if="index==0"
              role="button" aria-expanded="false" :aria-controls="index">{{ day.substring(4,12) }}(Today)</a>

              <a class="nav-link text-white" data-bs-toggle="collapse" :href="'#' + index.toString()" v-else
              role="button" aria-expanded="false" :aria-controls="index">{{ day.substring(4,12) }}</a>

            </li>
          </ul>
        </div>
        <div id="timeslots">
        <!-- {% for date, slots in slotsDict|dictsort %} -->
        <div class="collapse" data-bs-parent="#timeslots" v-for="(slot,index) in timeslots.slots" :id="index" >
          <div class="card card-body">
            <h5 class="card-title" style="margin-bottom: 10px;">{{ timeslots.days[index].substring(4,12) }}</h5>
            <div class="card-text mt-3">

                <p class="alert alert-sm alert-primary" style="width: 40%; margin: auto;" v-if="slot.length==0">No shows</p>

              <span v-else v-for="entry in slot" class="">
                    <button v-if="entry.avSeats == 0" class="btn btn-danger position-relative" title="No seats left">{{ entry.time }}
                      <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-primary">
                      {{ entry.avSeats }}</span></button>&emsp14;

                    <!-- {% elif (timeslot[1] | int) < 15 %} -->
                    <button class="btn btn-warning position-relative" v-else-if="entry.avSeats < 15" 
                    @click="setModalBody(entry,index)" data-bs-toggle="modal" data-bs-target="#priceModal">{{ entry.time }}
                      <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-primary">{{ entry.avSeats }}</span></button>&emsp14;

                    <button class="btn btn-success position-relative" v-else
                        @click="setModalBody(entry,index)" data-bs-toggle="modal" data-bs-target="#priceModal">{{ entry.time }}
                        <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-primary">{{ entry.avSeats }}</span></button>&emsp14;
                    
              </span>
            </div>
          </div>
        </div>
        </div>
      </div>
      <div style="margin: ;">
        <p v-if="error_message" class="badge bg-danger text-center me-4 mt-5">Error: {{ error_message }}</p>
      </div>
    </div>
</template>