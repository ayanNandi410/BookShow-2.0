<script setup>
const props = defineProps({
  id: String,
  name: String,
  rating: Number,
  duration: String,
  timestamp: String,
  tags: Array,
  languages: Array,
});
</script>

<template>
<div class="col">
          <div class="card p-3" style="width: 18rem; margin-right: 20px;">
            <div class="card-img-caption">
                <div class="d-flex justify-content-end mb-4">
                <img
                    src="@/assets/star-full.svg"
                    class="filter-orange" width="20"
                    v-for="(n, index) in parseInt(props.rating/2)"
                />
                <img
                    src="@/assets/star-empty.svg"
                    class="filter-orange" width="20"
                    v-for="(n, index) in 5 - parseInt(props.rating/2)"
                />
                </div>
                <div class="p-4">
                  <img
                    src="@/assets/movie.png"
                    class="card-img-top blurImage"
                    height="200"
                    alt="Movie"
                  />
                </div>
            </div>
            <div class="card-body">
              <h5 class="card-title">{{ props.name }}</h5>
              <div class="card-text mt-3">
                <span
                    class="badge bg-success mb-1"
                    style="margin: auto 2%"
                    v-for="tag in props.tags"
                    >{{ tag.name }}</span
                >&nbsp;<br />
                <span
                    class="badge bg-dark text-white mb-1"
                    style="margin: auto 2%"
                    v-for="lng in props.languages"
                    >{{ lng.name }}</span
                >
                <span class="badge bg-info text-white">{{ props.duration }}</span>&nbsp;
              </div>
            </div>
            <div class="card-footer text-muted">
                <p><img src="@/assets/calendar.svg"/> {{ props.timestamp.slice(0,22) }}</p>
              <a href="#" class="btn btn-sm btn-danger" data-bs-toggle="modal"
              @click="$emit('deleteShow',props.name,props.id)" data-bs-target="#deleteModal">Delete</a>&emsp14;
              <a href="#" class="btn btn-sm btn-warning" @click="$emit('updateShow',props.name,props.id)">Update</a><br/>
              <router-link to="/admin/allocateTimings" ><button class="btn btn-sm btn-success mt-2" @click="$emit('saveShow',props.id,props.name)">Add Timing</button></router-link>
            </div>
          </div>
        </div>
</template>

<style>
.filter-orange {
  filter: invert(86%) sepia(22%) saturate(4813%) hue-rotate(337deg)
    brightness(95%) contrast(108%);
}
</style>
 