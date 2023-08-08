<script>
import ToastMsg from '../components/toastMsg.vue'
import { fetchVenuesByName, updateTiming } from "../api";

export default {
    name: "updateTiming",
    data() {
        return {
            user: this.$store.getters.fetch_user_details,
            venue: { id: this.$store.state.venue.id, name: this.$store.state.venue.name },
            show: { id: this.$store.state.show.id, name: this.$store.state.show.name },
            searchVenues: [],
            timing: { id: this.$store.state.timing.id },
            venueName: "",
            date: "",
            time: "",
            seats: 10,
            price: 0.00,
            toastShow: false,
            header: "",
            head_end: "",
            message: "",
            type: "",
            loading: false,
        };
    },
    methods: {

        updateCurTiming() {
            const timing = {
                showId: this.show.id,
                venueId: this.venue.id,
                date: this.date,
                time: this.time,
                seats: this.seats,
                price: this.price
            }

            updateTiming(this.user.auth_token, timing, this.timing.id)
                .then(async res => {
                    const data = await res.json()
                    console.log(data);
                    this.type = 'error';
                    this.toastShow = true;
                    this.header = 'Add Timing';

                    if (!res.ok) {
                        this.message = data.error_message;
                        this.head_end = data.error_code;
                        this.loading = false;
                    }
                    else {
                        this.type = 'info';
                        this.message = 'Success';
                    }

                })
                .catch(e => {
                    this.message = e.data;
                    console.log("Fetch Error: " + e)
                }
                );
        },

        closeToast() {
            this.toastShow = false;
        },

        saveVenueCh(id, name) {
            this.$store.commit('set_choosen_venue', { id: id, name: name });
        },

        load_venues_by_name() {
            this.searchVenues = [];
            this.loading = true;

            fetchVenuesByName(this.user.auth_token, this.venueName)
                .then(async res => {
                    const data = await res.json()
                    console.log(data)

                    if (!res.ok) {
                        this.message = data.error_message;
                        this.loading = false;
                    }
                    else {
                        this.loading = false;
                        this.searchVenues = data;
                    }

                })
                .catch(e => {
                    this.loading = false;
                    console.log("Fetch Error: " + e)
                }
                );
        },
    },
    computed: {
        venueChoosen() {
            this.venue = { id: this.$store.state.venue.id, name: this.$store.state.venue.name };
            return this.venue;
        }
    },

    onMounted() {
        this.$store.commit('set_user_details_from_local');
        this.user = this.$store.getters.fetch_user_details;
    },

    components: { ToastMsg },
};
</script>

<template>
    <div class="body container vh-100">

        <ToastMsg v-bind:header="header" v-bind:head_end="head_end" v-bind:message="message" v-bind:type="type"
            v-if="toastShow" @close-toast="closeToast" />

        <div class="offcanvas offcanvas-bottom" tabindex="-1" id="chShowCanvas" aria-labelledby="offcanvasBottomLabel"
            style="min-height: 85%;">
            <div class="offcanvas-header">
                <h5 class="offcanvas-title" id="offcanvasBottomLabel">Choose Venue</h5>
                <button type="button" class="btn-close text-reset" data-bs-dismiss="offcanvas" aria-label="Close"></button>
            </div>
            <div class="offcanvas-body">
                <div id="searchBar">
                    <div class="row">
                        <div class="col-4">
                            <input class="form-control form-control-sm me-2" id="searchVenueName" v-model="venueName"
                                type="search" placeholder="Search for venues" aria-label="Search">
                        </div>
                        <div class="col-4">
                            <button class="btn btn-sm btn-outline-success" type="button"
                                @click="load_venues_by_name">Search</button>
                            <div style="margin: auto 50%;" v-if="loading">
                                <div class="spinner-border spinner-border-lg text-primary" role="status">
                                    <span class="visually-hidden">Loading...</span>
                                </div>
                            </div>
                        </div>
                    </div>
                    <br /><br />
                </div>
                <div v-if="searchVenues.length == 0">
                    <br /><br /><br />
                    <div class="col-6 justify-content-center" style="margin: auto;">
                        <h3 class="alert alert-primary mb-4 text-center">No Venues found</h3>
                    </div>
                </div>
                <div class="row row-cols-2 row-cols-sm-4 g-4" id="chooseShowCards" v-else>
                    <div class="col" v-for="venue in searchVenues">
                        <div class="card p-3" style="width: fit-content; margin-right: 20px">
                            <div class="card-body">
                                <h5 class="card-title">{{ venue.name }}</h5>
                                <div class="card-text mt-3">
                                    <p class="badge bg-success text-white"> Location: {{ venue.location }} , {{ venue.city
                                    }}</p>
                                    <p class="badge bg-success text-white"> Capacity: {{ venue.capacity }}</p>
                                    <button class="btn btn-primary mt-3" @click="saveVenueCh(venue.id, venue.name)"
                                        data-bs-dismiss="offcanvas">Choose Venue</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>


        <div class="row">
            <div class="col-12 col-sm-4">
                <h2>Update Timings</h2>
            </div>
            <div class="col-12 col-sm-2 offset-sm-6">
                <button class="btn btn-success" @click="$router.go(-1)">Go Back</button>
            </div>
        </div>
        <hr /><br />
        <div class="d-flex justify-content-center h-100">
            <form class="mt-4" onsubmit="return false;">
                <!-- Name input -->
                <input type="number" value="{{ vid }}" name="venue_id" style="display: none;">

                <div class="row mb-3">
                    <div class="col-12 col-sm-10">
                        <div class="input-group input-group-md mb-3">
                            <span class="input-group-text" name="showName">For Show</span>
                            <input type="text" class="form-control" name="showName" id="showName" placeholder="Not choosen"
                                v-model="show.name" aria-label="Show Name" readonly required>
                        </div>
                    </div>
                </div>

                <div class="row mb-3">
                    <div class="col-12 col-sm-10">
                        <div class="input-group input-group-md mb-3">
                            <span class="input-group-text" name="venueName">For Venue</span>
                            <input type="text" class="form-control" name="venueName" id="venueName"
                                v-model="venueChoosen.name" aria-label="venueName" readonly>
                        </div>
                    </div>
                    <div class="col-12 col-sm-2">
                        <button type="button" class="btn btn-success btn-md"
                            style="padding-left: 2.5rem; padding-right: 2.5rem;" data-bs-toggle="offcanvas"
                            data-bs-target="#chShowCanvas" aria-controls="chShowCanvas">Choose Venue</button>
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
                    <div class="col-10">
                        <div class="input-group input-group-md mb-3">
                            <span class="input-group-text">Release Date</span>
                            <input type="date" class="form-control" name="showReleaseDate" id="showReleaseDate"
                                aria-label="Show Release Date" min="{{ curDate }}" v-model="date" required>
                        </div>
                    </div>
                </div>

                <div class="row mb-3">
                    <div class="col-10">
                        <div class="input-group input-group-md mb-3">
                            <span class="input-group-text">Release Time</span>
                            <input type="time" class="form-control" name="showReleaseTime" id="showReleaseTime" min="06:00"
                                max="23:00" v-model="time" required>
                        </div>
                    </div>
                </div>

                <div class="row mb-3">
                    <div class="col-12 col-sm-8">
                        <div class="input-group input-group-md mb-3">
                            <span class="input-group-text">Number of Seats</span>
                            <input type="number" class="form-control" name="allocSeats" min="10" id="allocSeats"
                                aria-label="allocSeats" v-model="seats" required>
                        </div>
                    </div>
                </div>

                <div class="row mb-3">
                    <div class="col-10">
                        <div class="input-group input-group-md mb-3">
                            <span class="input-group-text">Ticket Price</span>
                            <input type="number" min="0.00" step=".01" class="form-control" name="showTicketPrice"
                                id="showTicketPrice" placeholder="450.00" v-model="price" aria-label="Show Ticket Price"
                                required>
                        </div>
                    </div>
                </div>
                <br/>
                <div class="row mb-3">
                    <div class="col-6 offset-sm-3">
                        <button class="btn btn-primary btn-md" style="padding-left: 2.5rem; padding-right: 2.5rem;"
                            @click="updateCurTiming">Allocate Show Timings</button>
                    </div>
                </div>
            </form>
        </div>
    </div>
</template>
