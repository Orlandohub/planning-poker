import { Redirect } from "react-router-dom";

import axios from 'axios'
import { capitalize } from 'lodash'


export const login = async (qs) => {
    const response = await axios.post(
        "http://localhost:8000/login/access-token",
        qs,
        {
            headers: {
             'accept': 'application/json',
             'Content-Type': 'application/x-www-form-urlencoded'
            }
        }        
    )
    const token_type = capitalize(response.data.token_type)
    const token = response.data.access_token
    localStorage.setItem("auth", `${token_type} ${token}`) 
    return localStorage.getItem("auth")
}


export const register = async (form_data) => {
    const response = await axios.post(
        "http://localhost:8000/users/signup",
        JSON.stringify(form_data),
        {
            headers: {
                'accept': 'application/json',
                'Content-Type': 'application/json'
            }
        }        
    )
    return response
}


export const logout = async (history) => {
    localStorage.removeItem("auth")
    history.push('/login')
}


export const currentUser = async () => {
    let response = null
    const token_bearer = localStorage.getItem("auth")

    if (!token_bearer) {
        return response
    }

    try{
        response = await axios.get(
            "http://localhost:8000/users/me",
            {
              headers: {
                'accept': 'application/json',
                'Authorization': token_bearer
              }
            } 
        )
    } catch(err) {
        console.log('err', err);
        return null
    }

    return response.data
}


export const isAuth = async () => {
    const response = await currentUser()
    return response && true
}

