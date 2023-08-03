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
        <img
          src="@/assets/hall.png"
          class="card-img-top blurImage"
          height="200"
          width="30"
          alt="..."
        />
      </div>
      <div class="card-body">
        <h5 class="card-title">{{ props.name }}</h5>
        <p class="card-text">
          <span
            class="badge rounded-pill bg-secondary"
            style="padding: 8px 10px"
            >{{ props.location }}, {{ props.city }}</span
          >
        </p>
        <form method="post" action="/user/venueHome">
          <input
            type="number"
            name="vid"
            :value="props.id"
            style="display: none"
          />
          <button type="submit" class="btn btn-primary">Explore</button>
        </form>
      </div>
    </div>
  </div>
</template>
