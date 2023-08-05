<script setup>
const props = defineProps({
  id: String,
  name: String,
  capacity: Number,
  location: String,
  city: String,
});
</script>

<template>
  <div class="col">
    <div class="card p-3" style="width: 18rem; margin-right: 20px">
      <div class="card-img-caption">
        <div class="d-flex justify-content-end">
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
          <span
            class="badge rounded-pill bg-secondary"
            style="padding: 8px 10px"
            >{{ props.location }}<span v-if="props.city">, {{ props.city }}</span></span
          >
        </p>
        <router-link :to="{ name: 'userVenueHome' }" @click="$emit('saveVenueChoice')" class="btn btn-primary">Explore</router-link>
      </div>
    </div>
  </div>
</template>
