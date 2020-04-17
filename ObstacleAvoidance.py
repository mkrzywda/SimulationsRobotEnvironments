from controller import Robot
from controller import Compass

# Get reference to the robot.
robot = Robot()

# Get simulation step length.
timeStep = int(robot.getBasicTimeStep())

# get robot's Compass device
compass = robot.getCompass("compass")
# enable the Compass
compass.enable(timeStep)

# Constants of the Thymio II motors and distance sensors.
maxMotorVelocity = 9.53  # 24
distanceSensorCalibrationConstant = 360 #360

# Get left and right wheel motors.
leftMotor = robot.getMotor("motor.left")
rightMotor = robot.getMotor("motor.right")

# Get frontal distance sensors.
outerLeftSensor = robot.getDistanceSensor("prox.horizontal.0")
centralLeftSensor = robot.getDistanceSensor("prox.horizontal.1")
centralSensor = robot.getDistanceSensor("prox.horizontal.2")
centralRightSensor = robot.getDistanceSensor("prox.horizontal.3")
outerRightSensor = robot.getDistanceSensor("prox.horizontal.4")

# Enable distance sensors.
outerLeftSensor.enable(timeStep)
centralLeftSensor.enable(timeStep)
centralSensor.enable(timeStep)
centralRightSensor.enable(timeStep)
outerRightSensor.enable(timeStep)

# Disable motor PID control mode.
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))

# Set ideal motor velocity.
initialVelocity = 0.95 * maxMotorVelocity # 0.7 # 90%

# Set the initial velocity of the left and right wheel motors.
leftMotor.setVelocity(initialVelocity)
rightMotor.setVelocity(initialVelocity)


while robot.step(timeStep) != -1:
    # Read values from four distance sensors and calibrate.
    outerLeftSensorValue = outerLeftSensor.getValue() / distanceSensorCalibrationConstant
    centralLeftSensorValue = centralLeftSensor.getValue() / distanceSensorCalibrationConstant
    centralSensorValue = centralSensor.getValue() / distanceSensorCalibrationConstant
    centralRightSensorValue = centralRightSensor.getValue() / distanceSensorCalibrationConstant
    outerRightSensorValue = outerRightSensor.getValue() / distanceSensorCalibrationConstant
    
    values = compass.getValues()    
    _in = 1  # jest ok 2,  prawie 1
    _ext = 1  # jest ok 2, prawie 1
    _lsens  = (outerLeftSensorValue/_ext + centralLeftSensorValue*_in)
    _rsens = (outerRightSensorValue/_ext + centralRightSensorValue*_in) - centralSensorValue*_in
    
    if _lsens == 0 and _rsens == 0:
        _lsens = _lsens + (values[0]**2)/values[0]
        
    _left = max(-9.53, min(initialVelocity - _rsens , maxMotorVelocity))
    _right = max(-9.53, min(initialVelocity - _lsens  , maxMotorVelocity))
    leftMotor.setVelocity(_left)
    rightMotor.setVelocity(_right)
