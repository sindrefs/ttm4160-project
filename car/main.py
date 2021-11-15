from MqttClient import MqttClient
from diddyborgv2.ttm4160_test import PerformContinousMove, PerformStop


def handleCommand(command):
    if command['command']:
        if (command['command'] == "go"):
            print(command)
            PerformContinousMove()
        elif (command['command'] == "stop"):
            PerformStop()
        elif (command['command'] == "backwards"):
            PerformContinousMove(direction="BACKWARDS")
        elif (command['command'] == "joystick"):
            joystickvalues = command['joystick']
            dir = "FORWARDS" if joystickvalues.y > 0 else "BACKWARDS"
            PerformContinousMove(joystickvalues.x, dir)


if __name__ == '__main__':
    client = MqttClient(handleCommand)
    client.startLoop()
