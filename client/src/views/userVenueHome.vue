<script>
import { fetchVenue, fetchShowsByVenue } from '../api';


export default {
    name: "userVenueHome",
    data() {
        return {
            user: this.$store.getters.fetch_user_details,
            venue: {},
            venueId: this.$store.state.venueId,
            shows: [],
            loading: false,
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

    fetchShows(){

        fetchShowsByVenue(this.user.auth_token, this.venueId)
            .then(async res =>  {
            const data = await res.json()
            console.log(data)

            if(!res.ok){
                console.log("Response Error");
            }
            else{
                this.shows = data;
            }
            
            })
            .catch(e => {
                this.showsLoading = false;
                console.log("Fetch Error: "+e)
                }
            ); 
    },

    },

    computed: {
    },

    components: { },

    beforeMount(){
        this.$store.commit('set_user_details_from_local');
        this.user = this.$store.getters.fetch_user_details;
        this.load_venue();
    },

    onMounted() {
        
    },

};
</script>

<template>
    <div class="body vh-100">

    <div class="offcanvas offcanvas-bottom" tabindex="-1" id="offcanvasBottom" 
        aria-labelledby="offcanvasBottomLabel" style="min-height: 80%;">
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
                <div class="col" v-for="show in shows">
                    <div class="card p-3" style="width: 15rem; margin-right: 20px">
                    <div class="card-body">
                        <h5 class="card-title">{{ show.name }}</h5>
                        <div class="card-text mt-3">
                        <span
                            class="badge bg-success mb-1"
                            style="margin: auto 2%"
                            v-for="tag in show.tags"
                            >{{ tag.name }}</span
                        >&nbsp;<br />
                        <span
                            class="badge bg-dark text-white mb-1"
                            style="margin: auto 2%"
                            v-for="lng in show.languages"
                            >{{ lng.name }}</span
                        ><br/>
                        <span class="badge bg-info text-white">{{ show.duration }}</span>&nbsp;
                        <span class="badge bg-warning text-dark mt-3">Rating: {{ show.rating }} / 10</span>
                        <router-link to="/user/buyTicket" class="btn btn-primary mt-3">Buy Tickets</router-link>
                        </div>
                    </div>
                    </div>
                </div>
            </div>
        </div>
      </div>

        <div class="container py-5 col-10">
            <h1 class="display-5 fw-bold">{{ venue.name }}</h1>
            <p class="col-md-8 fs-4 mt-4">{{ venue.description }}</p>
            <button class="btn btn-primary mt-4 btn-md" type="button" data-bs-toggle="offcanvas" @click="fetchShows"
        data-bs-target="#offcanvasBottom" aria-controls="offcanvasBottom">View all shows</button>
        </div>
    </div>
</template>