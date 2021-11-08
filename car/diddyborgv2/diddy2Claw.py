#!/usr/bin/env python
# coding: Latin-1

# Load library functions we want
import time
import os
import sys
import pygame
import ThunderBorg
import UltraBorg

# Re-direct our output to standard error, we need to ignore standard out to hide some nasty print statements from pygame
sys.stdout = sys.stderr

# Setup the ThunderBorg
TB = ThunderBorg.ThunderBorg()
#TB.i2cAddress = 0x15                  # Uncomment and change the value if you have changed the board address
TB.Init()
if not TB.foundChip:
    boards = ThunderBorg.ScanForThunderBorg()
    if len(boards) == 0:
        print 'No ThunderBorg found, check you are attached :)'
    else:
        print 'No ThunderBorg at address %02X, but we did find boards:' % (TB.i2cAddress)
        for board in boards:
            print '    %02X (%d)' % (board, board)
        print 'If you need to change the I²C address change the setup line so it is correct, e.g.'
        print 'TB.i2cAddress = 0x%02X' % (boards[0])
    sys.exit()
# Ensure the communications failsafe has been enabled!
failsafe = False
for i in range(5):
    TB.SetCommsFailsafe(True)
    failsafe = TB.GetCommsFailsafe()
    if failsafe:
        break
if not failsafe:
    print 'Board %02X failed to report in failsafe mode!' % (TB.i2cAddress)
    sys.exit()

# Setup the UltraBorg board
UB = UltraBorg.UltraBorg()              # Create a new UltraBorg object
UB.Init()                               # Set the board up (checks the board is connected)

# Settings for the joystick
axisUpDown = 1                          # Joystick axis to read for up / down position
axisUpDownInverted = False              # Set this to True if up and down appear to be swapped
axisLeftRight = 2                       # Joystick axis to read for left / right position
axisLeftRightInverted = False           # Set this to True if left and right appear to be swapped
buttonSlow = 8                          # Joystick button number for driving slowly whilst held (L2)
slowFactor = 0.5                        # Speed to slow to when the drive slowly button is held, e.g. 0.5 would be half speed
buttonFastTurn = 9                      # Joystick button number for turning fast (R2)
interval = 0.00                         # Time between updates in seconds, smaller responds faster but uses more processor time
buttonMeArmClawOpen = 7                 # Joystick button number to open the claw (D-Pad Left)
buttonMeArmClawClose = 5                # Joystick button number to close the claw (D-Pad Right)
buttonMeArmForward = 4                  # Joystick button number to move the MeArm forwards (D-Pad Up)
buttonMeArmBackward = 6                 # Joystick button number to move the MeArm backwards (D-Pad Down)
buttonMeArmUp = 12                      # Joystick button number to move the MeArm upwards (Triangle)
buttonMeArmDown = 14                    # Joystick button number to move the MeArm downwards (Cross)
buttonMeArmLeft = 15                    # Joystick button number to move the MeArm left (Square)
buttonMeArmRight = 13                   # Joystick button number to move the MeArm right (Circle)

# Power settings
voltageIn = 12.0                        # Total battery voltage to the ThunderBorg
voltageOut = 12.0 * 0.95                # Maximum motor voltage, we limit it to 95% to allow the RPi to get uninterrupted power

# Setup the power limits
if voltageOut > voltageIn:
    maxPower = 1.0
else:
    maxPower = voltageOut / float(voltageIn)

# Settings for the MeArm
servoMeArmClaw = 4                      # Servo index used for opening the claw
servoMeArmForwardBackward = 3           # Servo index used for moving the MeArm forward / backward
servoMeArmUpDown = 2                    # Servo index used for moving the MeArm up / down
servoMeArmLeftRight = 1                 # Servo index used for moving the MeArm left / right
meArmClaw = 0.0                         # Starting position for the claw
meArmForwardBackward = 0.0              # Starting position for the MeArm forward / backward
meArmUpDown = 0.0                       # Starting position for the MeArm up / down
meArmLeftRight = 0.0                    # Starting position for the MeArm left / right
rateMeArmClaw = 1.0                     # Movement speed for the claw
rateMeArmForwardBackward = 1.0          # Movement speed for the MeArm forward / backward
rateMeArmUpDown = 1.0                   # Movement speed for the MeArm up / down
rateMeArmLeftRight = 1.0                # Movement speed for the MeArm left / right
rateMeArmSlow = 0.2                     # Reduced movement speed when the drive slowly button is held

# Setup pygame and wait for the joystick to become available
TB.MotorsOff()
TB.SetLedShowBattery(False)
TB.SetLeds(0,0,1)
os.environ["SDL_VIDEODRIVER"] = "dummy" # Removes the need to have a GUI window
pygame.init()
#pygame.display.set_mode((1,1))
print 'Waiting for joystick... (press CTRL+C to abort)'
while True:
    try:
        try:
            pygame.joystick.init()
            # Attempt to setup the joystick
            if pygame.joystick.get_count() < 1:
                # No joystick attached, set LEDs blue
                TB.SetLeds(0,0,1)
                pygame.joystick.quit()
                time.sleep(0.1)
            else:
                # We have a joystick, attempt to initialise it!
                joystick = pygame.joystick.Joystick(0)
                break
        except pygame.error:
            # Failed to connect to the joystick, set LEDs blue
            TB.SetLeds(0,0,1)
            pygame.joystick.quit()
            time.sleep(0.1)
    except KeyboardInterrupt:
        # CTRL+C exit, give up
        print '\nUser aborted'
        TB.SetCommsFailsafe(False)
        TB.SetLeds(0,0,0)
        sys.exit()
print 'Joystick found'
joystick.init()
TB.SetLedShowBattery(True)
ledBatteryMode = True

# Make a function to control a specific servo
def SetServoPosition(servo, position):
    if servo == 1:
        UB.SetServoPosition1(position)
    elif servo == 2:
        UB.SetServoPosition2(position)
    elif servo == 3:
        UB.SetServoPosition3(position)
    elif servo == 4:
        UB.SetServoPosition4(position)
    else:
        print 'Servo index %d is not available' % (servo)

# Set acceleration values
accelScale = 0.001
accelRate = 1.005
accelMeArmClaw = rateMeArmClaw * accelScale
accelMeArmForwardBackward = rateMeArmForwardBackward * accelScale
accelMeArmUpDown = rateMeArmUpDown * accelScale
accelMeArmLeftRight = rateMeArmLeftRight * accelScale

# Set the initial MeArm positions
SetServoPosition(servoMeArmClaw, meArmClaw)
SetServoPosition(servoMeArmForwardBackward, meArmForwardBackward)
SetServoPosition(servoMeArmUpDown, meArmUpDown)
SetServoPosition(servoMeArmLeftRight, meArmLeftRight)

try:
    print 'Press CTRL+C to quit'
    driveLeft = 0.0
    driveRight = 0.0
    running = True
    hadEvent = False
    upDown = 0.0
    leftRight = 0.0
    # Loop indefinitely
    while running:
        # Get the latest events from the system
        hadEvent = False
        events = pygame.event.get()
        # Handle each event individually
        for event in events:
            if event.type == pygame.QUIT:
                # User exit
                running = False
            elif event.type == pygame.JOYBUTTONDOWN:
                # A button on the joystick just got pushed down
                hadEvent = True
            elif event.type == pygame.JOYAXISMOTION:
                # A joystick has been moved
                hadEvent = True
            if hadEvent:
                # Read axis positions (-1 to +1)
                if axisUpDownInverted:
                    upDown = -joystick.get_axis(axisUpDown)
                else:
                    upDown = joystick.get_axis(axisUpDown)
                if axisLeftRightInverted:
                    leftRight = -joystick.get_axis(axisLeftRight)
                else:
                    leftRight = joystick.get_axis(axisLeftRight)
                # Apply steering speeds
                if not joystick.get_button(buttonFastTurn):
                    leftRight *= 0.5
                # Determine the drive power levels
                driveLeft = -upDown
                driveRight = -upDown
                if leftRight < -0.05:
                    # Turning left
                    driveLeft *= 1.0 + (2.0 * leftRight)
                elif leftRight > 0.05:
                    # Turning right
                    driveRight *= 1.0 - (2.0 * leftRight)
                # Check for button presses
                if joystick.get_button(buttonSlow):
                    driveLeft *= slowFactor
                    driveRight *= slowFactor
                # Set the motors to the new speeds
                TB.SetMotor1(driveLeft  * maxPower)
                TB.SetMotor2(driveRight * maxPower)
            # Adjust the MeArm positions every loop
            if joystick.get_button(buttonSlow):
                meArmSpeed = rateMeArmSlow
            else:
                meArmSpeed = 1.0
            # Claw open / close
            if joystick.get_button(buttonMeArmClawClose):
                meArmClaw += accelMeArmClaw * meArmSpeed
                accelMeArmClaw *= accelRate
                if meArmClaw > 1.0:
                    meArmClaw = 1.0
                SetServoPosition(servoMeArmClaw, meArmClaw)
            elif joystick.get_button(buttonMeArmClawOpen):
                meArmClaw -= accelMeArmClaw * meArmSpeed
                accelMeArmClaw *= accelRate
                if meArmClaw < -1.0:
                    meArmClaw = -1.0
                SetServoPosition(servoMeArmClaw, meArmClaw)
            else:
                accelMeArmClaw = rateMeArmClaw * accelScale
            # MeArm forward / backward
            if joystick.get_button(buttonMeArmForward):
                meArmForwardBackward += accelMeArmForwardBackward * meArmSpeed
                accelMeArmForwardBackward *= accelRate
                if meArmForwardBackward > 1.0:
                    meArmForwardBackward = 1.0
                SetServoPosition(servoMeArmForwardBackward, meArmForwardBackward)
            elif joystick.get_button(buttonMeArmBackward):
                meArmForwardBackward -= accelMeArmForwardBackward * meArmSpeed
                accelMeArmForwardBackward *= accelRate
                if meArmForwardBackward < -1.0:
                    meArmForwardBackward = -1.0
                SetServoPosition(servoMeArmForwardBackward, meArmForwardBackward)
            else:
                accelMeArmForwardBackward = rateMeArmForwardBackward * accelScale
            # MeArm up / down
            if joystick.get_button(buttonMeArmUp):
                meArmUpDown += accelMeArmUpDown * meArmSpeed
                accelMeArmUpDown *= accelRate
                if meArmUpDown > 1.0:
                    meArmUpDown = 1.0
                SetServoPosition(servoMeArmUpDown, meArmUpDown)
            elif joystick.get_button(buttonMeArmDown):
                meArmUpDown -= accelMeArmUpDown * meArmSpeed
                accelMeArmUpDown *= accelRate
                if meArmUpDown < -1.0:
                    meArmUpDown = -1.0
                SetServoPosition(servoMeArmUpDown, meArmUpDown)
            else:
                accelMeArmUpDown = rateMeArmUpDown * accelScale
            # MeArm left / right
            if joystick.get_button(buttonMeArmLeft):
                meArmLeftRight += accelMeArmLeftRight * meArmSpeed
                accelMeArmLeftRight *= accelRate
                if meArmLeftRight > 1.0:
                    meArmLeftRight = 1.0
                SetServoPosition(servoMeArmLeftRight, meArmLeftRight)
            elif joystick.get_button(buttonMeArmRight):
                meArmLeftRight -= accelMeArmLeftRight * meArmSpeed
                accelMeArmLeftRight *= accelRate
                if meArmLeftRight < -1.0:
                    meArmLeftRight = -1.0
                SetServoPosition(servoMeArmLeftRight, meArmLeftRight)
            else:
                accelMeArmLeftRight = rateMeArmLeftRight * accelScale
        # Change LEDs to purple to show motor faults
        if TB.GetDriveFault1() or TB.GetDriveFault2():
            if ledBatteryMode:
                TB.SetLedShowBattery(False)
                TB.SetLeds(1,0,1)
                ledBatteryMode = False
        else:
            if not ledBatteryMode:
                TB.SetLedShowBattery(True)
                ledBatteryMode = True
        # Wait for the interval period
        time.sleep(interval)
except KeyboardInterrupt:
    # CTRL+C exit
    print '\nUser shutdown'
finally:
    # Disable all drives
    TB.MotorsOff()
    TB.SetCommsFailsafe(False)
    TB.SetLedShowBattery(False)
    TB.SetLeds(0,0,0)
    print
