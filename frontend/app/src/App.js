import React from 'react';
import {
  BrowserRouter as Router,
  Switch,
  Route
} from "react-router-dom";

import PrivateRoute from './components/privateRoute'
import Register from './screens/register'
import Login from './screens/login'
import Poll from './screens/poll'

import './App.css';
import 'papercss/dist/paper.min.css'

function App() {
  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <Switch>
            <Route path="/register">
              <Register />
            </Route>
            <Route path="/login">
              <Login />
            </Route>
            <PrivateRoute path="/">
              <Poll />
            </PrivateRoute>
          </Switch>
        </header>
      </div>
    </Router>
  );
}

export default App;
