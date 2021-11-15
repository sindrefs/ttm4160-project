import paho.mqtt.client as mqtt
import json

CAR_CONTROLS_TOPIC = "ttm4160/carcontrols"
BROKER_URL = "broker.hivemq.com"


class MqttClient:
    def __init__(self, commandHandler):
        self.commandHandler = commandHandler
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(BROKER_URL, 1883, 60)

    def on_connect(self, client, userdata, flags, rc):
        print("Connected")
        client.subscribe(CAR_CONTROLS_TOPIC)

    def on_message(self, client, userdata, message):
        commandReceived = json.loads(
            str(message.payload.decode("utf-8", "ignore")))
        self.dispatch(commandReceived)
        print(commandReceived)

    def startLoop(self):
        self.client.loop_forever()

    def dispatch(self, command):
        self.commandHandler(command)


if __name__ == '__main__':

    def testCommandHandler(command):
        print("received command: %s" % command)

    client = MqttClient(testCommandHandler)
    client.startLoop()
