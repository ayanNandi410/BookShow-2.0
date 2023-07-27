
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

export function fetchCities() {
  const requestOptions = {
    method: "GET",
    headers: { "Content-Type": "application/json" }
  };
  return fetch(`${API_URL}city/all`, requestOptions)
}

export function fetchVenues(city) {
  const requestOptions = {
    method: "GET",
    headers: { "Content-Type": "application/json" },
  };
  return fetch(`${API_URL}venues/byCity/${city}`, requestOptions)
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