from MqttClient import MqttClient
from diddyborgv2.ttm4160_test import PerformDrive, PerformStop


def handleCommand(command):
    if (command['command'] == "go"):
        print(command)
        PerformDrive(1)
    elif (command['command'] == "stop"):
        PerformStop()


if __name__ == '__main__':
    client = MqttClient(handleCommand)
    client.startLoop()
