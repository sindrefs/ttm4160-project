from MqttClient import MqttClient
from diddyborgv2.ttm4160_test import PerformContinousMove, PerformStop


def handleCommand(command):
    if (command['command'] == "go"):
        print(command)
        PerformContinousMove()
    elif (command['command'] == "stop"):
        PerformStop()
    elif (command['command'] == "backwards"):
        PerformContinousMove(direction="BACKWARDS")
    elif (command['command'].joystick):
        PerformContinousMove(direction="BACKWARDS")

if __name__ == '__main__':
    client = MqttClient(handleCommand)
    client.startLoop()
