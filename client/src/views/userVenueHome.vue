<script>
import UserShowCard from '../components/UserShowCard.vue'
import { fetchCities, fetchVenues, fetchVenuesByName } from '../api';

export default {
    name: "userVenueHome",
    data() {
        return {
            user: this.$store.getters.fetch_user_details,
            venue: {},
            venueId: this.$route.params.id,
            shows: [],
            loading: false,
            showsLoading: false,
        };
    },

    methods: {
        load_venue() {

            fetchVenue(this.user.auth_token, this.venueId)
                .then(async res => {
                    const data = await res.json()
                    console.log(data)

                    if (!res.ok) {
                        this.error_message = data.error_message;
                        this.error_code = data.error_code;
                    }
                    else {

                        this.venue = data;
                    }

                })
                .catch(e => {
                    console.log("Fetch Error: " + e)
                }
                );
        },

    },

    computed: {
        loading() {
            return this.loading;
        },
    },

    components: { UserShowCard },

    beforeMount() {
        this.load_venue();
    },

    onMounted() {
        this.$store.commit('set_user_details_from_local');
        this.user = this.$store.getters.fetch_user_details;
    },

};
</script>

<template>
    <div class="body vh-100">
    <div class="container py-5 col-8">
        <h1 class="display-5 fw-bold">{{ venue.name }}</h1>
        <p class="col-md-8 fs-4">{{ venue.description }}</p>
        <button class="btn btn-primary btn-md" type="button" data-bs-toggle="offcanvas" 
        data-bs-target="#offcanvasBottom" aria-controls="offcanvasBottom">View all shows</button>
    </div>
    <div class="offcanvas offcanvas-bottom" tabindex="-1" id="offcanvasBottom" aria-labelledby="offcanvasBottomLabel">
      <div class="offcanvas-header">
        <h5 class="offcanvas-title" id="offcanvasBottomLabel">Available shows</h5>
        <button type="button" class="btn-close text-reset" data-bs-dismiss="offcanvas" aria-label="Close"></button>
      </div>
      <div class="offcanvas-body">
            <div v-if="shows.length==0">
                <br/><br/><br/>
                <div class="col-6 justify-content-center" style="margin: auto;">
                  <h3 class="alert alert-primary mb-4 text-center">No Shows Available</h3>
                </div>
            </div>
          <div class="row row-cols-1 row-cols-sm-4 g-4" v-else>
            <UserShowCard v-for="show in shows" 
                v-bind:id=show.id.toString()
                v-bind:name="show.name"
                v-bind:duration="show.duration"
                v-bind:rating="show.rating"
                v-bind:tags="show.tags"
                v-bind:languages="show.languages"
                @deleteShow="deleteShowModal"/>
          </div>
      </div>
    </div>
    </div>
</template>