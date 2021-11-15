import { Joystick } from 'react-joystick-component';
import React, { useState } from 'react';
import './_Remote-Controller.scss';



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
      body: JSON.stringify({ joystick: event })
    })
  }

  const handleStop = (event) => {
    console.log(event)
  }

  return (
    <div>

      <Joystick size={100} throttle={200} baseColor="#232C33" stickColor="red" move={handleMove} stop={handleStop}></Joystick>

    </div>
  );
}

export default RemoteController;
