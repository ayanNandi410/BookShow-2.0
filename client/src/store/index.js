import Vuex from 'vuex'

import { fetch_auth_token } from '../api'

//Vue.use(Vuex)

const state = {
  // single source of data
  auth_token: "",
  error_message: "",
  active_user: false,
  user_type: "",
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
    state.user_type = payload.user_type;
    console.log("User Details updated...")
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
  }

}

const getters = {
  // reusable data accessors

}

const store = new Vuex.Store({
  state,
  actions,
  mutations,
  getters
})

export default store