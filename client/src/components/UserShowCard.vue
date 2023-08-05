<script setup>
const props = defineProps({
  id: String,
  name: String,
  rating: Number,
  duration: String,
  tags: Array,
  languages: Array,
});
</script>

<template>
  <div class="col">
    <div class="card p-3" style="width: 18rem; margin-right: 20px">
      <div class="card-img-caption">
        <div class="d-flex justify-content-end">
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
          height="250"
          width="100"
          alt="..."
          />
        </div>
      </div>
      <div class="card-body">
        <h5 class="card-title">{{ props.name }}</h5>
        <div class="card-text">
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
          <span class="badge bg-info text-white">{{ props.duration }}</span
          >&nbsp;
        </div>
      </div>
      <div class="card-footer text-muted">
        <button
          type="button"
          class="btn btn-sm btn-warning"
          data-bs-toggle="modal"
          data-bs-target="#reviewsModal"
          @click="$emit('showReviews')"
        >
          Reviews</button
        >&emsp13;

        <button
          type="button"
          class="btn btn-sm btn-success"
          data-bs-toggle="offcanvas"
          data-bs-target="#chVenueCanvas"
          aria-controls="chVenueCanvas"
          @click="$emit('showVenues')"
        >
          Venues
        </button>
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
