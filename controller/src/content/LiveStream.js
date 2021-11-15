import React from 'react'
import useWebSocket from 'react-use-websocket'

const socketUrl = "ws://ttm41-bfflo-17c606og763lz-1083556350.eu-west-1.elb.amazonaws.com"

const LiveStream = () => {
    const { lastMessage: socketData } = useWebSocket(socketUrl)

    if (socketData === null) {
        return null
    }

    const imageData = JSON.parse(socketData.data).image.replace("b'", "").replace("'", "")

    return <img src={`data:image/jpg;base64,${imageData}`} />

}

export default LiveStream