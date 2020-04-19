import React, { useState } from 'react'
import { useForm } from 'react-hook-form'
import axios from 'axios'


function Register() {
  const { register, handleSubmit, errors } = useForm()
  const [invalidCredentials, setInvalidCredentials] = useState(false)

  const onSubmit = async data => {
    try {
      const response = await axios.post(
        "http://localhost:8000/users/signup",
        JSON.stringify(data),
        {
          headers: {
            'accept': 'application/json',
            'Content-Type': 'application/json'
          }
        }        
      )
      console.log("response", response)
      setInvalidCredentials(false)
    } catch (error) {
      setInvalidCredentials(true)
    }
  }

  return (
    <div>
      <form className="baseForm" onSubmit={handleSubmit(onSubmit)}>
        <span className={
          `baseInputError ${invalidCredentials ? "text-danger" : null}`
        }>
          {invalidCredentials ? "Username already exists" : null}
        </span>
        <div className="baseInput">
          <input name="username" placeholder="Username" ref={register({
            required: true,
            pattern: /^[a-z0-9_-]{1,25}$/i
          })} />
          {
            errors.username?.type === "required" ||
            errors.username?.type === "pattern" ?
            <span className="baseInputError text-danger">
              {errors.username?.type === "required" && "This field is required"}
              {errors.username?.type === "pattern" && "Only alphanumeric and _ allowed"}
            </span> :
            <span className="baseInputError">
            </span>
          }

        </div>
        <div className="baseInput">
          <input type="password" name="password" placeholder="Password" ref={
            register({
              required: true,
              pattern: /^[a-z0-9_-]{1,25}$/i
            })} />
            {
              errors.password?.type === "required" ||
              errors.password?.type === "pattern" ?
              <span className="baseInputError text-danger">
                {errors.password?.type === "required" && "This field is required"}
                {errors.password?.type === "pattern" && "Only alphanumeric and _ allowed"}
              </span> :
              <span className="baseInputError">
              </span>
            }
        </div>
        <input type="submit" value="Register" />
      </form>
      <hr/>
      <p>Or Login</p>
    </div>
  )
}

export default Register