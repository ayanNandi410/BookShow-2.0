<script>
import { fetchTimings, deleteTiming } from '../api'
import ToastMsg from '../components/toastMsg.vue'


export default {
    name: "adminTimings",
    data() {
        return {
            user : this.$store.getters.fetch_user_details,
            timings: [],
            startDate: "",
            endDate: "",
            show: { name: this.$route.query.showName, id: this.$route.query.showId },
            venue: { name: this.$route.query.venueName, id: this.$route.query.venueId },
            loading: false,
            timingChoice: "",
            toastShow: false,
            header: "",
            head_end: "",
            message: "",
            type: "",
            deleteResult: false,
        };
    },
    methods: {
        
        closeToast() {
            this.toastShow = false;
        },

        updateTiming(timing) {
            this.$store.commit('set_choosen_venue', { id: this.venue.id, name: this.venue.name });
            this.$store.commit('set_choosen_show', { id: this.show.id, name: this.show.name });
            this.$store.commit('set_choosen_timing', { id: timing.id });
        },

        load_all_timings() {
            this.loading = true;
            fetchTimings(this.user.auth_token,{
                sid: this.show.id,
                vid: this.venue.id,
                startDate: this.startDate,
                endDate: this.endDate
                })
                .then(async res => {
                    const data = await res.json()
                    //console.log(data)
                    this.loading = false;

                    if (!res.ok) {
                        this.head_end = data.error_code;
                        this.message = data.error_message;
                    }
                    else {
                        this.timings = data;
                    }

                })
                .catch(e => {
                    this.loading = false;
                    console.log("Fetch Error: " + e)
                }
                );
        },

        deleteTimingModal(timing) {
            this.timingChoice = { date: timing.date, time: timing.time, id: timing.id }
        },

        deleteChoosenTiming() {
            this.type = "error";
            this.toastShow = true;
            this.header = "Delete Timing";

            deleteTiming(this.user.auth_token,this.timingChoice.id)
                .then(async res => {
                    const data = await res.json()
                    console.log(data)
                    this.deleteResult = true;

                    if (!res.ok) {
                        this.head_end = data.error_code;
                        this.message = data.error_message;
                    }
                    else {
                        this.type = "info";
                        this.timings = [];
                        this.load_all_timings();
                        this.message = "Success"
                    }

                })
                .catch(e => {
                    this.error_message = e.data;
                    console.log("Fetch Error: " + e)
                }
                );
        },

    },

    computed: {
        loading() {
            return this.loading;
        },
        showsLoading() {
            return this.showsLoading;
        },
        deleteRes() {
            return this.deleteResult;
        }
    },

    components: { ToastMsg },

    beforeMount() {
        //this.load_all_cities();
    },

    onMounted(){
    this.$store.commit('set_user_details_from_local');
    this.user = this.$store.getters.fetch_user_details;
    }

};
</script>


<template>
    <div class="container body">

        <ToastMsg 
        v-bind:header="header" 
        v-bind:head_end="head_end" 
        v-bind:message="message" 
        v-bind:type="type" 
        v-if="toastShow"
        @close-toast="closeToast" />

        <!-- Delete Modal -->
        <div class="modal fade" id="deleteModal" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
            <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                <h1 class="modal-title fs-5" id="exampleModalLabel">Delete Timing</h1>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body" id="deleteModalBody">
                    <p>Are you sure you wish to delete timing: </p>
                    <p>Date: {{ timingChoice.date }}</p>
                    <p>Time: {{ timingChoice.time }}</p><br/>
                </div>
                <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                <a href="#" @click="deleteChoosenTiming" data-bs-toggle="modal" data-bs-target="#deleteModal"
                 id="alcDeleteBt" class="btn btn-primary">Delete Timing</a>
                </div>
            </div>
            </div>
        </div>

            <div class="row">
                <div class="col-12 col-sm-4">
                <h2>Show Timings</h2>
                </div>
                <div class="col-12 col-sm-2 offset-sm-6">
                    <router-link to="/admin/venues" class="btn btn-success"> Go Back</router-link>
                </div>
            </div>
            <hr/><br/>
              <div class="d-flex justify-content-center">
                <h4 class="alert alert-primary text-center" style="width: 100%;">Timeslots</h4>
              </div>
                <br/>
                <div class="row text-center">
                  <div class="col-12 col-sm-6">
                    <h5 class="alert alert-success">Show : {{ show.name }}</h5>
                  </div>
                  <div class="col-12 col-sm-6">
                    <h5 class="alert alert-success">Venue : {{ venue.name }}</h5>
                  </div>
                </div>
                <hr/>
                <div class="container">
                    <form onsubmit="return false;">
                        <div class="row d-flex justify-content-center">
                            <div class="col-12 col-sm-3">
                                <h4> Enter Range : </h4>
                            </div>
                            <div class="col-12 col-sm-4">
                                <div class="input-group input-group-md">
                                    <span class="input-group-text">Start Date</span>
                                    <input type="date" class="form-control" name="startDate" v-model="startDate" 
                                    id="startDate" aria-label="date" required>
                                </div>
                            </div>
                            <div class="col-12 col-sm-4">
                                <div class="input-group input-group-md">
                                    <span class="input-group-text">End Date</span>
                                    <input type="date" class="form-control" name="endDate" v-model="endDate"
                                    id="endDate" aria-label="date" required>
                                </div>
                            </div>
                            <div class="col-12 col-sm-1">
                                <button @click="load_all_timings" class="btn btn-success">Search</button>
                            </div>
                        </div>
                    </form>
                </div>

                <hr/><br/><br/>

                <div v-if="loading" style="margin: auto;">
                    <div class="spinner-border spinner-border-lg text-primary" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                </div>

                <!-- {% if emptyAlloc is defined %} -->
                <div class="d-flex justify-content-center" v-if="timings.length==0">
                  <h2 class="alert alert-primary text-center" style="width: 60%;">No slots alloted</h2>
                </div>

                <div class="list-group">
                    <!-- {% for alloc in allocations %} -->
                    <div href="#" class="list-group-item list-group-item-action" v-for="timing in timings">
                        <div class="d-flex w-100 justify-content-between mb-3">
                          <h5 class="mb-1">Date : {{ timing.date }}</h5>
                          <button type="button" class="btn btn-sm btn-danger" @click="deleteTimingModal(timing)"
                          data-bs-toggle="modal" data-bs-target="#deleteModal">Delete Timing</button>
                        </div>
                        <div class="d-flex w-100 justify-content-between mb-3">
                            <h5 class="mb-1">Time : {{ timing.time }}</h5>
                            <router-link to="/admin/timing/update"><a class="btn btn-sm btn-warning" @click="updateTiming(timing)">Update Timing</a></router-link>
                        </div>
                        <div class="d-flex w-100 justify-content-between">
                            <p class="mb-1">Seats remaining : <b>{{ timing.avSeats }} out of {{ timing.totSeats }} </b></p>
                            <small>Price per seat: <b>{{ timing.price }}</b></small>
                        </div>
                    </div>
                    <!-- {% endfor %} -->
                </div>
                <!-- {% endif %} -->
    </div>
</template>