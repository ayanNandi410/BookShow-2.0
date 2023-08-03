
import axios from 'axios'

const API_URL = 'http://127.0.0.1:5000/api/'
const BASE_URL = 'http://127.0.0.1:5000/'

export function fetch_auth_token(user_details){
    const requestOptions = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(user_details)
      };
    return fetch(`${BASE_URL}login?include_auth_token`, requestOptions)
}

export function register_user(user_details){
    const requestOptions = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(user_details)
      };
    return fetch(`${BASE_URL}register`, requestOptions)
}

export function logout_user(){
  const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
    };
  return fetch(`${BASE_URL}logout`, requestOptions)
}


export function fetchCities() {
  const requestOptions = {
    method: "GET",
    headers: { "Content-Type": "application/json" }
  };
  return fetch(`${API_URL}city/all`, requestOptions)
}

export function fetchVenues(token, city, user_type) {
  const requestOptions = {
    method: "GET",
    headers: { "Content-Type": "application/json", "Authentication-Token": token },
  };
  if(user_type=='admin'){
    return fetch(`${API_URL}venuesforAdmin/byCity/${city}`, requestOptions)
  }
  else{
    return fetch(`${API_URL}venuesforUser/byCity/${city}`, requestOptions)
  }
  
}

export function fetchVenuesByName(token, name) {
  const requestOptions = {
    method: "GET",
    headers: { "Content-Type": "application/json", "Authentication-Token": token },
  };
    return fetch(`${API_URL}venueByName/${name}`, requestOptions)
  
}

export function deleteVenue(token,id) {
  const requestOptions = {
    method: "DELETE",
    headers: { "Content-Type": "application/json", "Authentication-Token": token },
  };
  return fetch(`${API_URL}venue/${id}`, requestOptions)
}

export function addVenue(token,venue) {
  const requestOptions = {
    method: "POST",
    headers: { "Content-Type": "application/json", "Authentication-Token": token },
    body: JSON.stringify(venue),
  };
  return fetch(`${API_URL}venue`, requestOptions)
}

export function addShow(token,show) {
  const requestOptions = {
    method: "POST",
    headers: { "Content-Type": "application/json", "Authentication-Token": token },
    body: JSON.stringify(show),
  };
  return fetch(`${API_URL}show`, requestOptions)
}

export function deleteShow(token,id) {
  const requestOptions = {
    method: "DELETE",
    headers: { "Content-Type": "application/json", "Authentication-Token": token },
  };
  return fetch(`${API_URL}show/${id}`, requestOptions)
}

export function fetchPopularShows(token) {
  const requestOptions = {
    method: "GET",
    headers: { "Content-Type": "application/json", "Authentication-Token": token },
  };
    return fetch(`${API_URL}popularShows`, requestOptions)
  
}

export function fetchShowsByVenue(token,id) {
  const requestOptions = {
    method: "GET",
    headers: { "Content-Type": "application/json", "Authentication-Token": token },
  };
    return fetch(`${API_URL}show/byVenue/${id}`, requestOptions)
  
}

export function fetchTimings(details) {
  const requestOptions = {
    method: "GET",
    headers: { "Content-Type": "application/json" }
  };
    return fetch(`${API_URL}timingWithRange?startDate=${details.startDate}
                &endDate=${details.endDate}&sid=${details.sid}&vid=${details.vid}`, requestOptions)
  
}

export function deleteTiming(id) {
  const requestOptions = {
    method: "DELETE",
    headers: { "Content-Type": "application/json" },
  };
  return fetch(`${API_URL}timing/${id}`, requestOptions)
}

export function fetchSurvey(surveyId) {
  return axios.get(`${API_URL}/surveys/${surveyId}/`)
}

export function saveSurveyResponse(surveyResponse) {
  return axios.put(`${API_URL}/surveys/${surveyResponse.id}/`, surveyResponse)
}

export function postNewSurvey(survey) {
  return axios.post(`${API_URL}/surveys/`, survey)
}