from MqttClient import MqttClient
from diddyborgv2.ttm4160_test import PerformContinousMove, PerformStop


def handleCommand(command):
    if (command['command'] == "go"):
        print(command)
        PerformContinousMove()
    elif (command['command'] == "stop"):
        PerformStop()


if __name__ == '__main__':
    client = MqttClient(handleCommand)
    client.startLoop()
