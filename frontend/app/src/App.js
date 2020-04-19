import React from 'react';
import Register from './screens/register'
import './App.css';
import 'papercss/dist/paper.min.css'

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>
          <span role="img" aria-label="Joker">🃏</span>
            Planning Poker
          <span role="img" aria-label="Joker">🃏</span>
        </h1>
        <p><b>Collaborative planning app!</b></p>
        <Register /> 
      </header>
    </div>
  );
}

export default App;
