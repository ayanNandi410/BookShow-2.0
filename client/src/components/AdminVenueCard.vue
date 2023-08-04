<script setup>
const props = defineProps({
  id: String,
  name: String,
  capacity: Number,
  location: String,
  description: String,
  timestamp: String,
});
</script>

<template>
    <div class="col">
        <div class="card p-3" style="width: 18rem; margin-right: 20px;">
            <div class="card-img-caption">
                <div class="d-flex justify-content-end mb-4">
                  <span class="card-text badge rounded-pill bg-primary flex-row-reverse"
                    >Capacity : {{ props.capacity }}</span
                  >
                </div>
                <div class="p-4">
                  <img
                  src="@/assets/hall.png"
                  class="card-img-top blurImage"
                  height="200"
                  width="30"
                  alt="..."
                  />
                </div>
            </div>
          <div class="card-body">
            <h5 class="card-title">{{ props.name }}</h5>
            <p class="card-text">
              <span class="badge rounded-pill bg-secondary" style="padding: 8px 10px;">{{ props.location }}</span>&emsp13;
            </p>   
            <a href="#" class="btn btn-primary" @click="$emit('displayShows',this.name,this.id)"
            data-bs-toggle="offcanvas" data-bs-target="#offcanvasShows" aria-controls="offcanvasShows">Shows</a>&emsp14;
            <a href="#" class="btn btn-primary" @click="$emit('exportVeueDet',this.name,this.id)">Export</a>&emsp14;
          </div>
          <div class="card-footer text-muted">
            <p><img src="@/assets/calendar.svg"/> {{ props.timestamp.slice(0,22) }}</p>

            <a href="#" class="btn btn-sm btn-danger" 
            data-bs-toggle="modal" data-bs-target="#deleteModal" 
            @click="$emit('deleteVenue',this.name,this.id)">Delete</a>&emsp14;

            <a href="#" class="btn btn-sm btn-warning">Update</a><br/>
          </div>
        </div>
      </div>
</template>
