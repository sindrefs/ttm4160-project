
const http = require("http")
const express = require("express")
const WebSocket = require("ws")

const app = express()

app.use(express.json())

const server = http.createServer(app)

const websocketServer = new WebSocket.Server({ server })

const port = 80

const send = (msg) => {
    websocketServer.clients.forEach(client => {
        client.send(JSON.stringify(msg))
    })
}

app.post("/image", (req, res) => {
    send(req.body)
    res.send({ result: "ok" })
})

app.get("/health/", (req, res) => {
    res.send({ status: "Ok" })
})

server.listen(port, () => {
    console.log(`Listening on port: ${port}`)
})