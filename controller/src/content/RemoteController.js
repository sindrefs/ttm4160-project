import { Joystick } from 'react-joystick-component';
import React, { useState } from 'react';
import mqtt from 'mqtt';


const RemoteController = () => {
  /*const { client } = useMqttState();

  function handleClick() {
    console.log("handleClick called")
    return client.publish('esp32/led', "testmessage heiehei");
  }
  */



  const handleMove = (event) => {
    console.log(event)
    fetch("https://rf7lsu4mv5.execute-api.eu-west-1.amazonaws.com/prod/", {
      method: "POST",
      body: JSON.stringify({joystick: event})
    })
  }

  const handleStop = (event) => {
    console.log(event)
  }

  return (
    <div>
      REMOTE CONTROLLER

      {/*<button type="button" onClick={() => handleClick}>
        Test send
  </button>*/}


      <Joystick size={100} throttle={200} baseColor="red" stickColor="blue" move={handleMove} stop={handleStop}></Joystick>

    </div>
  );
}

export default RemoteController;
