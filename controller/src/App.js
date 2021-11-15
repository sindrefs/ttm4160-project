import React, { useState } from 'react';
import logo from './logo.svg';
import './App.scss';
import RemoteController from './content/RemoteController';
import LiveStream from './content/LiveStream';



function App() {
  console.log({ state: "ready" })

  const handleEmergency = () => {
    console.log("Emergency stop called")
    fetch("https://rf7lsu4mv5.execute-api.eu-west-1.amazonaws.com/prod/", {
      method: "POST",
      body: JSON.stringify({ command: "stop" })
    })
      .then(response => console.log(response))
      .catch(err => console.log(err));
  }

  return (

    <div className="app">
      <div className="header-box">
        <div className="header-text">
          Super-car-controller! 🏎

        </div>
      </div>

      <div className="container">

        <div className="stream">
        </div>

        <div className="joystick">
          <RemoteController />
        </div>

        <button onClick={handleEmergency}>EMERGENCY STOP!</button>

      </div>


    </div >
  );
}

export default App;
