<script>
import UserVenueCard from '../components/UserVenueCard.vue'
import { fetchVenues, fetchVenuesByName } from '../api';

export default {
    name: "userSearchVenues",
    data() {
        return {
            user: this.$store.getters.fetch_user_details,
            venues: [],
            showsForVenue: [],
            loading: false,
            showsLoading: false,
            venueName: "",
            venueChoice: "",
        };
    },
    methods: {
        saveVenueCh(id){
            this.$store.commit('set_choosen_venue', { id: id });
        },

        load_venues_by_name() {
            this.venues = [];
            this.loading = true;

            fetchVenuesByName(this.user.auth_token,this.venueName)
                .then(async res => {
                    const data = await res.json()
                    console.log(data)

                    if (!res.ok) {
                        this.error_message = data.error_message;
                        this.error_code = data.error_code;
                        this.loading = false;
                    }
                    else {
                        this.loading = false;
                        this.venues = data;
                    }

                })
                .catch(e => {
                    this.loading = false;
                    console.log("Fetch Error: " + e)
                }
                );
        },

        fetchVenuesforCity() {
            var e = document.getElementById("cityChoice");
            var city = e.value;
            this.loading = true;

            fetchVenues(city, 'admin')
                .then(async res => {
                    const data = await res.json()
                    console.log(data)

                    if (!res.ok) {
                        this.error_message = data.error_message;
                        this.error_code = data.error_code;
                        this.loading = false;
                    }
                    else {
                        this.venues = data;
                        this.loading = false;
                    }

                })
                .catch(e => {
                    console.log("Fetch Error: " + e)
                }
                );
        },

    },
    computed: {
    },

    components: { UserVenueCard },

    beforeMount() {
        //this.load_all_cities();
    },

    onMounted() {
        this.$store.commit('set_user_details_from_local');
        this.user = this.$store.getters.fetch_user_details;
    },

};
</script>


<template>
    <div class="body container" style="min-height: 100%;">

    <div class="row">
        <div class="col-12 col-sm-3">
            <h2 style="display: inline;">Venues<span v-if="venues.length!=0"> found : </span></h2>
        </div>
        <div class="col-12 col-sm-4">
                <div class="input-group mb-3">
                    <label class="input-group-text" for="inputGroupSelect01">Venue Name</label>
                    <input class="form-control form-control-sm" name="searchVenueName" type="search" 
                    placeholder="Search for venues" aria-label="Search" v-model="venueName">
                    <button class="btn btn-success" @click="load_venues_by_name">Search</button>
                </div>
        </div>
        <hr />
    </div>
    <br /><br />

        <div style="margin: auto 50%;">
            <div class="spinner-border spinner-border-lg text-primary" role="status" v-if="loading">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>

        <h2 class="alert alert-primary text-center" style="margin: 8% 10% 20%;" 
        v-if="venues.length == 0">Did not find any venue. Try again..</h2>

        <div class="row row-cols-md-3 row-cols-sm-1 g-3" v-else>
            <UserVenueCard v-for="venue in venues" 
            v-bind:id=venue.id.toString() 
            v-bind:name=venue.name
            v-bind:capacity=venue.capacity 
            v-bind:location=venue.location
            v-bind:city=venue.city
            @saveVenueChoice="saveVenueCh(venue.id.toString())" />
        </div>
    </div>
</template>