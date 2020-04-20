import React from 'react';
import {
  BrowserRouter as Router,
  Switch,
  Route
} from "react-router-dom";
import { CookiesProvider } from 'react-cookie';

import PrivateRoute from './components/privateRoute'
import Register from './screens/register'
import Login from './screens/login'
import Poll from './screens/poll'

import './App.css';
import 'papercss/dist/paper.min.css'

function App() {
  return (
    <CookiesProvider>
      <Router>
        <div className="App">
          <Switch>
            <Route path="/register">
              <Register />
            </Route>
            <Route path="/login">
              <Login />
            </Route>
            <PrivateRoute path="/poll/:slug">
              <Poll />
            </PrivateRoute>
          </Switch>
        </div>
      </Router>
    </CookiesProvider>
  );
}

export default App;
