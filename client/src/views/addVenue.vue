<script setup>
</script>

<template>
<div class="body">

<div class="container">
    <h2>Add new Venue</h2><hr/><br/>
  <div class="d-flex justify-content-center align-items-center h-100">

      <form class="mt-4" action="{{ url_for('admin.addVenue')}}" method="post" onsubmit="return formValidate();">  
        <!-- Name input -->
        <div class="row mb-3">
            <div class="col-12 col-sm-6">
                <div class="input-group input-group-lg mb-3">
                    <span class="input-group-text" name="venueName">Venue Name</span>
                    <input type="text" class="form-control" name="venueName" id="venueName" placeholder="Allen Hall" value="" aria-label="venueName" required>
                </div>
            </div>
            <div class="col-12 col-sm-6">
                <div class="input-group input-group-lg mb-3">
                    <span class="input-group-text">Venue Location</span>
                    <input type="text" class="form-control" name="venueLocation" id="venueLocation" placeholder="Beleghata" value="" aria-label="venueLocation" required>
                </div>
            </div>
        </div>
        <div class="col-12 col-sm-6">
            <div class="input-group input-group-lg mb-3">
                <span class="input-group-text">Venue City</span>
                <input type="text" class="form-control" name="venueCity" id="venueCity" placeholder="Kolkata" value="" aria-label="venueCity" required>
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
                    <input type="number" class="form-control" name="venueCapacity" id="venueCapacity" placeholder="450" value="" aria-label="venueCapacity" required>
                    <div id="capCheck" class="invalid-feedback">&emsp;Capacity of Venue too less</div>
                </div>
            </div>
        </div>

        <div class="row mb-3">
            <div class="input-group input-group-lg mb-3">
                <span class="input-group-text">Venue Description</span>
                <textarea class="form-control" name="venueDescription" id="venueDescription" 
                aria-label="With textarea" placeholder="At least 50 characters" required></textarea>
                <div id="descCheck" class="invalid-feedback">&emsp;At least 50 characters are necessary</div>
            </div>
        </div>

        <div class="row mb-3">
            <div class="col-4 offset-5">
                <button type="submit" class="btn btn-primary btn-lg"
                style="padding-left: 2.5rem; padding-right: 2.5rem;">Register Venue</button>
            </div>
        </div>

      </form>
  </div>
</div>
</div>
</template>