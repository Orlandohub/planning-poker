import React, { useState, useEffect } from "react";
import {
  Route,
  Redirect,
} from "react-router-dom";

import { isAuth } from '../../utils/auth'


const PrivateRoute = ({ children, ...rest }) => {
    const [auth, setAuth] = useState(false)
    const [loading, setLoading] = useState(true)

    const getAuth = async () => {
      const res = await isAuth()
      setAuth(res)
      setLoading(false)
    };

    useEffect(() => {
      getAuth();
    }, []);

    if (loading) {
        return null
    }

    if (auth) {
        return (
            <Route
                {...rest}
                render={({ location }) => children}
            />
        )
    }
    
    return (
        <Route
            {...rest}
            render={({ location }) =>
                <Redirect
                    to={{
                        pathname: "/login",
                        state: { from: location }
                    }}
                />

            }
        />
    );
}

export default PrivateRoute