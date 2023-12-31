
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

export function user_addRole(email){
  const requestOptions = {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    };
  return fetch(`${BASE_URL}addRole/user/${email}`, requestOptions)
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

export function fetchVenue(token, id) {
  const requestOptions = {
    method: "GET",
    headers: { "Content-Type": "application/json", "Authentication-Token": token },
  };
    return fetch(`${API_URL}user/venue/${id}`, requestOptions)
  
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

export function updateVenue(token,venue) {
  const requestOptions = {
    method: "PUT",
    headers: { "Content-Type": "application/json", "Authentication-Token": token },
    body: JSON.stringify(venue),
  };
  return fetch(`${API_URL}venue`, requestOptions)
}

export function exportVenue(token, id) {
  const requestOptions = {
    method: "GET",
    headers: { "Content-Type": "application/json", "Authentication-Token": token },
  };
    return fetch(`${API_URL}exportVenue/${id}`, requestOptions)
  
}

export function downloadVenueCSV(name){
      axios({
        url: `${API_URL}venue/downloadCSV/${name}`, // Download File URL Goes Here
        method: 'GET',
        responseType: 'blob',
        headers: {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': ' GET, PUT, POST, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Origin, Content-Type, X-Auth-Token',
            'Access-Control-Allow-Credentials': 'false',
        },
    }).then((res) => {
        var FILE = window.URL.createObjectURL(new Blob([res.data]));
        var docUrl = document.createElement('x');
        docUrl.href = FILE;
        docUrl.setAttribute('download', name+'_Details.csv');
        document.body.appendChild(docUrl);
        docUrl.click();
    });
}

export function fetchVenuesByShow(token,id,city) {
  const requestOptions = {
    method: "GET",
    headers: { "Content-Type": "application/json", "Authentication-Token": token },
  };
    return fetch(`${API_URL}venue/byShow/${id}?city=${city}`, requestOptions)
  
}


export function addShow(token,show) {
  const requestOptions = {
    method: "POST",
    headers: { "Content-Type": "application/json", "Authentication-Token": token },
    body: JSON.stringify(show),
  };
  return fetch(`${API_URL}show`, requestOptions)
}

export function updateShow(token,show) {
  const requestOptions = {
    method: "PUT",
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


export function filterShows(token,details) {
  const requestOptions = {
    method: "POST",
    headers: { "Content-Type": "application/json", "Authentication-Token": token },
    body: JSON.stringify(details)
  };
    return fetch(`${API_URL}filterShow`, requestOptions)
  
}

export function fetchShowsByName(token,name) {
  const requestOptions = {
    method: "GET",
    headers: { "Content-Type": "application/json", "Authentication-Token": token },
  };
    return fetch(`${API_URL}showByName/${name}`, requestOptions)
  
}

export function fetchShowsByVenue(token,id) {
  const requestOptions = {
    method: "GET",
    headers: { "Content-Type": "application/json", "Authentication-Token": token },
  };
    return fetch(`${API_URL}show/byVenue/${id}`, requestOptions)
  
}

export function fetchTimings(token,details) {
  const requestOptions = {
    method: "GET",
    headers: { "Content-Type": "application/json", "Authentication-Token": token }
  };
    return fetch(`${API_URL}timingWithRange?startDate=${details.startDate}
                &endDate=${details.endDate}&sid=${details.sid}&vid=${details.vid}`, requestOptions)
  
}

export function addTiming(token,timing) {
  const requestOptions = {
    method: "POST",
    headers: { "Content-Type": "application/json", "Authentication-Token": token },
    body: JSON.stringify(timing),
  };
  return fetch(`${API_URL}timing`, requestOptions)
}

export function updateTiming(token,timing,id) {
  const requestOptions = {
    method: "PUT",
    headers: { "Content-Type": "application/json", "Authentication-Token": token },
    body: JSON.stringify(timing),
  };
  return fetch(`${API_URL}timing/${id}`, requestOptions)
}

export function deleteTiming(token,id) {
  const requestOptions = {
    method: "DELETE",
    headers: { "Content-Type": "application/json", "Authentication-Token": token },
  };
  return fetch(`${API_URL}timing/${id}`, requestOptions)
}

export function fetchTimeslots(token,details) {
  const requestOptions = {
    method: "GET",
    headers: { "Content-Type": "application/json" , "Authentication-Token": token }
  };
    return fetch(`${API_URL}timing/sevenDays?sid=${details.sid}&vid=${details.vid}`, requestOptions)
  
}

export function fetchBooking(token,email) {
  const requestOptions = {
    method: "GET",
    headers: { "Content-Type": "application/json", "Authentication-Token": token },
  };
    return fetch(`${API_URL}booking/${email}`, requestOptions)
  
}

export function registerBooking(token, details) {
  const requestOptions = {
    method: "POST",
    headers: { "Content-Type": "application/json", "Authentication-Token": token },
    body: JSON.stringify(details)
  };
    return fetch(`${API_URL}booking`, requestOptions)
  
}

export function fetchReviews(token,sid) {
  const requestOptions = {
    method: "GET",
    headers: { "Content-Type": "application/json", "Authentication-Token": token },
  };
    return fetch(`${API_URL}review/${sid}`, requestOptions)
  
}

export function addReview(token,details) {
  const requestOptions = {
    method: "POST",
    headers: { "Content-Type": "application/json", "Authentication-Token": token },
    body: JSON.stringify(details)
  };
    return fetch(`${API_URL}review`, requestOptions)
}
