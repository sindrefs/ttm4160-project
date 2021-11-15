import React, { useState } from 'react';
import logo from './logo.svg';
import './App.scss';
import RemoteController from './content/RemoteController';
import LiveStream from './content/LiveStream';



function App() {
  return (

    <div className="app">
      <div className="header-box">
        <div className="header-text">
          Super-car-controller! 🏎

        </div>
      </div>

      <div className="container">
        <div className="joystick">
          <RemoteController />

        </div>
        <LiveStream />
      </div>


    </div >
  );
}

export default App;
