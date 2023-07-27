<script>
import ShowCard from "../components/ShowCard.vue";
import VenueCard from "../components/VenueCard.vue";

export default {
  name: "Ping",
  data() {
    return {
      msg: "",
      tags: ["Funny", "Thriller"],
      languages: ["English", "Hindi"],
      rating: 3,
    };
  },
  methods: {
    fetchMessage() {
      fetch("http://localhost:5173/ping")
        .then((res) => res.text())
        .then((data) => {
          this.msg = data;
          console.log(data);
        })
        .catch((error) => {
          console.error("Returned Error:", error);
        });
    },
  },
  created() {
    this.fetchMessage();
  },
  components: { ShowCard, VenueCard },
};
</script>

<template>
  <div class="container">
    <button type="button" class="btn btn-primary">{{ msg }}</button>
    <ShowCard
      name="RamShayam"
      v-bind:rating="rating"
      duration="3 hrs"
      v-bind:tags="tags"
      v-bind:languages="languages"
    />
    <VenueCard name="Hall" location="Howrah" capacity="340" id="2" />
  </div>
</template>
