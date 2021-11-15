import React from 'react'
import useWebSocket from 'react-use-websocket'

const socketUrl = "ws://localhost:9000"

const LiveStream = () => {
    const { lastMessage: socketData } = useWebSocket(socketUrl)

    if (socketData === null) {
        return null
    }

    const imageData = JSON.parse(socketData.data).image.replace("b'", "").replace("'", "")

    return <img src={`data:image/jpg;base64,${imageData}`} />

}

export default LiveStream