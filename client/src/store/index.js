import Vuex from 'vuex'

//Vue.use(Vuex)

const state = {
  // single source of data
  auth_token: "",
  name: "",
  email: "",
  username: "",
  error_message: "",
  active_user: false,
  user_type: "",
  venue: {},
  show: {},
  timing: {},
  notifications: [],
}

const actions = {
  // asynchronous operations
    async load_auth_token(context, user_details){
        console.log("In load_auth_token")
        
    },

    async error_message_clear(context){
      context.commit('empty_error_message');
    },

    toggle_current_user(context){
      context.commit('toggle_user');
    }
}

const mutations = {
  // isolated data mutations

  set_user_details(state, payload){
    state.auth_token = payload.auth_token;
    state.name = payload.name;
    state.username = payload.username;
    state.email = payload.email;
    state.user_type = payload.type;
    console.log("User Details updated...")
  },

  set_user_details_from_local(state){
    state.auth_token = localStorage.auth_token;
    state.name = localStorage.name;
    state.username = localStorage.username;
    state.email = localStorage.email;
    state.user_type = localStorage.type;
    console.log("User Details updated from Local Storage...")
  },

  set_error_message(state, payload){
    state.error_message = payload.error_message;
    console.log("New Error Message: "+state.error_message)
  },

  empty_error_message(state){
    state.error_message = "";
    console.log("Error Message Cleared")
  },

  toggle_user(state){
    state.active_user = !state.active_user
    console.log(" active_user toggled")
  },

  set_choosen_venue(state, payload){
    state.venue ={ id: payload.id, name: payload.name }; 
    console.log(" venue saved")
  },

  set_choosen_show(state, payload){
    state.show ={ id: payload.id, name: payload.name }; 
    console.log(" show saved")
  },

  set_choosen_timing(state, payload){
    state.timing ={ id: payload.id }; 
    console.log(" timing saved")
  },

  set_notif(state, payload){
    state.notifications.push({ message: payload.message });
  }

}

const getters = {
  fetch_user_details(state){
    return {
      auth_token: state.auth_token,
      name: state.name,
      email: state.email,
      username: state.username,
      type: state.type
    }
  }

}

const store = new Vuex.Store({
  state,
  actions,
  mutations,
  getters
})

export default store