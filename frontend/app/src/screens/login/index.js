import React, { useState } from 'react'
import {
  useHistory,
  useLocation
} from "react-router-dom";
import querystring from 'querystring'

import AuthBaseHeader from '../../components/authBaseHeader'
import AuthBaseForm from '../../components/authBaseForm'
import { login } from '../../utils/auth'


function Login() {
  const [invalidCredentials, setInvalidCredentials] = useState(false)
  let history = useHistory();
  let location = useLocation();

  const onSubmit = async data => {
    const qs = querystring.stringify(data)
    try {
      await login(qs)
      setInvalidCredentials(false)
    } catch (error) {
      setInvalidCredentials(true)
      return null
    }

    let { from } = location.state || { from: { pathname: "/" } }
    history.replace(from)
  }

  return (
    <div>
      <AuthBaseHeader />
      <AuthBaseForm
        formType="Login"
        invalidCredentials={invalidCredentials}
        onSubmit={onSubmit}
      />
      <hr/>
      <p>Or Register</p>
    </div>
  )
}

export default Login