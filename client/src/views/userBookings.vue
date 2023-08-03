<script>
    function updateRating(val) {
          document.getElementById('ratingValue').innerHTML=val; 
          let value = parseInt(val);
          console.log(value);
        if(value < 4)
        {
            document.getElementById('ratingValue').classList.remove("bg-primary","bg-success","bg-warning","bg-danger");
            document.getElementById('ratingValue').classList.add("bg-danger");
        }        
        else if(value > 7)
        {
            document.getElementById('ratingValue').classList.remove("bg-primary","bg-success","bg-warning","bg-danger");
            document.getElementById('ratingValue').classList.add("bg-success");
        }
        else{
            document.getElementById('ratingValue').classList.remove("bg-primary","bg-success","bg-warning","bg-danger");
            document.getElementById('ratingValue').classList.add("bg-warning");
        }
    }

    export default {
  name: "userBookings",
  data() {
    return {
        bookings: [],
    };
  },
  methods: {
    
  },
  created() {
    
  },
  components: { },
};
</script>

<template>
    
<!-- Review Modal -->
<div class="modal fade" id="reviewModal" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
    <div class="modal-dialog">
      <form method="post" action="/user/review/add">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5" id="reviewModalTitle">Add Review</h1>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body" id="reviewModalBody">
            <input type="number" id="showId" name="showId" style="display: none;">
            <div class="col-12 mb-4">
              <div class="form-floating">
                <input type="text" class="form-control" name="showName" id="showName" readonly/>
                  <label for="showName">Show Name</label>
              </div>
            </div>
            <div class="col-12 col-sm-8">
              <label for="userRating" class="form-label">Rating : <span id="ratingValue" class="badge bg-primary text-white" on="changeColour();">5</span></label>
              <input type="range" class="form-range" min="0" max="10" value="5" step="1" 
              name="userRating" id="userRating" onchange="updateRating(this.value);" required>
          </div><br/>
          <div class="col-12">
              <div class="form-floating">
                  <textarea class="form-control" name="userComment" id="userComment"
                  placeholder="Leave a comment here(within 200 characters)" rows="10" required></textarea>
                  <label for="userComment">Comments</label>
              </div>
          </div>

        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
          <button type="submit" id="submitReview" class="btn btn-primary" data-bs-dismiss="modal">Submit Review</button>
        </div>
      </div>
    </form>
    </div>
  </div>

<div class="container body">
    <h2>Bookings</h2><hr/>
    <br/>

    <div class="vh-100">  
 
      <h2 class="text-center alert alert-primary" v-if="bookings.length==0">No booking done yet</h2>

        <div class="list-group" v-else>
            <div href="#" class="list-group-item list-group-item-action" v-for="booking in bookings">
                <div class="d-flex w-100 justify-content-between">
                  <h5 class="mb-1">Show : {{ booking.show.name }}</h5>
                  <small class="text-muted">{{ booking.timestamp }}</small>
                </div>
                <div class="d-flex w-100 justify-content-between">
                    <p class="mb-1">Venue : {{ booking.venue.name }}</p>
                    <small>Total Price : <b>{{ booking.totPrice }}</b></small>
                </div>
                <div class="d-flex w-100 justify-content-between">
                    <p class="mb-1">Show Timing : {{ booking.allocation.timeslot }}</p>
                    <small>Seats checked out: <b>{{ booking.allocSeats }}</b></small>
                </div>
                <div class="text-center">
                    <button type="button" class="btn btn-warning" 
                    data-bs-toggle="modal" data-bs-target="#reviewModal">Add Review</button>
                </div>
            </div>
          </div>
    </div>
  </div>
</template>