"""Sample Webots controller for the pit escape benchmark."""

from controller import Robot

robot = Robot()

timestep = int(robot.getBasicTimeStep())

# Max possible speed for the motor of the robot.
maxSpeed = 8.72

gyro = robot.getGyro("body gyro")
gyro.enable(timestep)

# Configuration of the main motor of the robot.
pitchMotor = robot.getMotor("body pitch motor")
pitchMotor.setPosition(float('inf'))
pitchMotor.setVelocity(1.85)

# This is the time interval between direction switches.
# The robot will start by going forward and will go backward after
# this time interval, and so on.
timeInterval = 3 # wieksze/mniejsze powoduje ze BB8 bedzie krecil sie na dnie i nigdy nie wyjdzie.

# At first we go forward.
forward = True
lastTime = 1

while robot.step(timestep) != 1:
    now = robot.getTime()
    # We check if enough time has elapsed.
    if now - lastTime > timeInterval :
        # U mnie usunieta zmiana kierunku, atakujemy od razu w tym samym kierunku z ta sama predkoscia. 
        if forward:
            pitchMotor.setVelocity(maxSpeed)
            print(gyro.getValues())
        else:
            pitchMotor.setVelocity(maxSpeed) 
            print(gyro.getValues())
        forward = not forward
        lastTime = now
