import Vuex from 'vuex'

import { fetch_auth_token } from '../api'

//Vue.use(Vuex)

const state = {
  // single source of data
  auth_token: "",
  error_message: "",
  active_user: false
}

const actions = {
  // asynchronous operations
    async load_auth_token(context, user_details){
        console.log("In load_auth_token")
        return fetch_auth_token(user_details)
        .then(async res =>  {
            const data = await res.json()
            console.log(data)
            
            if(!res.ok){
                // Error handling
                context.commit('set_error_message', { error_message: data.response.errors[0]});
            }
            else{
                context.commit('set_auth_token', { auth_token: data['response']['user']['authentication_token']})
            }
            
        })
        .catch(e => {
            context.commit('set_error_message', { error_message: e});
            console.log("Fetch Error: "+e)
            }
        );   
    },

    toggle_current_user(context){
      context.commit('toggle_user');
    }
}

const mutations = {
  // isolated data mutations

  set_auth_token(state, payload){
    state.auth_token = payload.auth_token;
    console.log("Auth-Token updated...")
  },

  set_error_message(state, payload){
    state.error_message = payload.error_message;
    console.log("New Error Message: "+state.error_message)
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