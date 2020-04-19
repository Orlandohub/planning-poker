import React, { useState } from 'react'
import { useHistory, Link } from "react-router-dom";
import querystring from 'querystring'

import AuthBaseHeader from '../../components/authBaseHeader'
import AuthBaseForm from '../../components/authBaseForm'
import { register, login } from '../../utils/auth'


function Register() {
  const [invalidCredentials, setInvalidCredentials] = useState(false)
  const history = useHistory();

  const onSubmit = async data => {
    // Register new user, if already exists pass error msg and exit
    try {
        await register(data)
        setInvalidCredentials(false)
    } catch (error) {
        setInvalidCredentials(true)
        return null
    }

    // If registration successful, login
    const qs = querystring.stringify(data)
    await login(qs)

    // And redirect to home after login
    history.push("/poll/home");
  }

  return (
    <div>
        <AuthBaseHeader />
        <AuthBaseForm
            formType="Register"
            invalidCredentials={invalidCredentials}
            onSubmit={onSubmit}
        />
      <hr/>
      <p>or <Link to="/login">Login</Link></p>
    </div>
  )
}

export default Register