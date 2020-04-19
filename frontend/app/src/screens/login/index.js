import React, { useState } from 'react'
import {
  useHistory,
  useLocation,
  Link
} from "react-router-dom";
import { useCookies } from 'react-cookie';
import querystring from 'querystring'

import AuthBaseHeader from '../../components/authBaseHeader'
import AuthBaseForm from '../../components/authBaseForm'
import { login } from '../../utils/auth'


function Login() {
  const [invalidCredentials, setInvalidCredentials] = useState(false)
  const [cookies, setCookie] = useCookies(['X-Authorization']);

  let history = useHistory();
  let location = useLocation();

  const onSubmit = async data => {
    const qs = querystring.stringify(data)
    try {
      const token = await login(qs)
      setCookie('X-Authorization', token, { path: '/' })
      setInvalidCredentials(false)
    } catch (error) {
      setInvalidCredentials(true)
      return null
    }

    let { from } = location.state || { from: { pathname: "/poll/home" } }
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
      <p>or <Link to="/register">Register</Link></p>
    </div>
  )
}

export default Login