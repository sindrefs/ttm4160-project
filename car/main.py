from MqttClient import MqttClient
from diddyborgv2.ttm4160_test import PerformDrive


def handleCommand(command):
    if (command['command'] == "go"):
        print(command)
        PerformDrive(1)


if __name__ == '__main__':
    client = MqttClient(handleCommand)
    client.startLoop()
