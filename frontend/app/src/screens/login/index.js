import React, { useState } from 'react'
import { useForm } from 'react-hook-form'
import axios from 'axios'
import querystring from 'querystring'
import { capitalize } from 'lodash'

function Login() {
  const { register, handleSubmit, errors } = useForm()
  const [invalidCredentials, setInvalidCredentials] = useState(false)

  const onSubmit = async data => {
    const qs = querystring.stringify(data)
    try {
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
      localStorage.setItem("auth", ` ${token_type} ${token}`)
    } catch (error) {
      setInvalidCredentials(true)
    }
  }

  return (
    <div>
      <form onSubmit={handleSubmit(onSubmit)}>
        {invalidCredentials ? "Username or Password Incorrect" : null}
        <input name="username" ref={register({
          required: true,
          pattern: /^[a-z0-9_-]{1,25}$/i
        })} />
        {errors.username?.type === "required" &&
           "This field is required"}
         {errors.username?.type === "pattern" &&
           "Only alphanumeric and _ allowed"}
        <input type="password" name="password" ref={register({ required: true })} />
        {errors.password && <span>This field is required</span>}
        
        <input type="submit" value="Login" />
      </form>
      <hr/>
      <p>Or Register</p>
    </div>
  )
}

export default Login