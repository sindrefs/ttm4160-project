import React, { useState } from 'react';
import logo from './logo.svg';
import './App.css';
import RemoteController from './content/RemoteController';
import LiveStream from './content/LiveStream';



function App() {
  return (

    <div className="App">

      <p>
        Hei Petter!
      </p>
      <RemoteController />
      <LiveStream />

    </div >
  );
}

export default App;
