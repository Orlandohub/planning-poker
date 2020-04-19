import React from 'react'
import PropTypes from 'prop-types'

import { useForm } from 'react-hook-form'

import './styles.css'


function AuthBaseForm({onSubmit, invalidCredentials, formType})  {
    const { register, handleSubmit, errors } = useForm()

    return (
        <form className="baseForm" onSubmit={handleSubmit(onSubmit)}>
          <span className={
            `baseInputError ${invalidCredentials ? "text-danger" : null}`
          }>
            {invalidCredentials && formType === "Login" ? "Invalid Credentials" : null}
            {invalidCredentials && formType === "Register" ? "Username already exists" : null}
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
          <button type="submit">{formType}</button>
        </form>
    )
}

AuthBaseForm.propTypes = {
  onSubmit: PropTypes.func.isRequired,
  invalidCredentials: PropTypes.bool.isRequired,
  formType: PropTypes.string.isRequired
}

export default AuthBaseForm
