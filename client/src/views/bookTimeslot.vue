<script>
import { fetchTimeslots } from '../api'

export default {
  name: "userTimeslots",
  data() {
    return {
        showName: this.$store.state.show.name,
        venueName: this.$store.state.venue.name,
        showId: this.$store.state.show.id,
        venueId: this.$store.state.venue.id,
        timeslots: {},
    };
  },
  methods: {
    fetchAllTimeslots() {
      this.loading = true;
      console.log("inside fetch booking");

      fetchTimeslots({ sid: this.showId, vid: this.venueId })
        .then(async res => {
          const data = await res.json()
          this.header = "Get Timeslots"

          if (!res.ok) {
            this.message = data.error_message;
            this.head_end = data.error_code;
            this.loading = false;
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
    countTimeslots(){
      let count = 0;

      if(this.timeslots=={})
      {
        return 0;
      }

      for(x in 7)
      {
        if(this.timeslots.slots[x]==[])
        {
          count++;
        }
      }
      return count;
    }
  },
  components: { },

  beforeMount(){
    this.fetchAllTimeslots();
  }
};
</script>

<template>
    <!-- Ticket Price Modal -->
<div class="modal fade" id="priceModal" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h1 class="modal-title fs-5" id="priceModalTitle">Slot Details</h1>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body" id="priceModalBody">

      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
        <a href="#" id="bookBt" class="btn btn-primary">Book Tickets</a>
      </div>
    </div>
  </div>
</div>

<div class="body container" style="margin-top: 6%; padding-bottom: 25%;">
  <div class="row text-center">
    <h4>Choose your timeslot</h4>`<br/>
  </div>
    <div class="row text-center">
      <div class="col-12 col-sm-6">
        <h5 class="alert alert-success">Show: {{ showName }}</h5>
      </div>
      <div class="col-12 col-sm-6">
        <h5 class="alert alert-success">Venue: {{ venueName }}</h5>
      </div>
    </div><hr/>

      <br/><br/><h4 class="alert alert-success text-center" v-if="countTimeslots">No slots Available in this week.<br/> Will be added soon..</h4>

    <div class="card text-center" style="width: fit-content; margin: auto;">
        <div class="card-header" style="background-color: #1f87c8;">
          <p class="card-text text-white">Choose Day from below</p>
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
            <div class="card-text">

                <p class="alert alert-sm alert-primary" style="width: 40%; margin: auto;" v-if="slot.length==0">No shows</p>

              <div v-else v-for="entry in slot" class="">
                    <button v-if="entry.avSeats == 0" class="btn btn-danger position-relative" disabled>{{ entry.time }}
                      <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-primary">
                      {{ entry.avSeats }}</span></button>&emsp14;

                    <!-- {% elif (timeslot[1] | int) < 15 %} -->
                    <button class="btn btn-warning position-relative" v-else-if="entry.avSeats < 15" 
                    onclick=" setModalBody();" 
                    data-bs-toggle="modal" data-bs-target="#priceModal">{{ entry.time }}
                      <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-primary">{{ entry.avSeats }}</span></button>&emsp14;

                    <button class="btn btn-success position-relative" v-else
                        onclick=" setModalBody();"
                         data-bs-toggle="modal" data-bs-target="#priceModal">{{ entry.time }}
                        <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-primary">{{ entry.avSeats }}</span></button>&emsp14;
                    
              </div>
            </div>
          </div>
        </div>
        </div>
      </div>
</div>
</template>