import math
from colorama import Fore
#import camera
import motors
import tools
#import go_to
#import odometry
import random
import time
    
def testKinematics():
	v1 = round(random.random(), 3)
	v2 = round(random.random(), 3)
	print("v1 = ", v1)
	print("v2 = ", v2)
	x, theta = tools.direct_kinematics(v1, v2)
	print("x = ", x)
	print("theta = ", theta)
	v1bis, v2bis = tools.inverse_kinematic(x, theta)
	v1bis = round(v1bis, 3)
	v2bis = round(v2bis, 3)
	print("v1bis = ", v1bis)
	print("v2bis = ", v2bis)
	if v1 == v1bis and v2 == v2bis:
		return True
	return False

def testTurnLeft():
	m = motors.Motors()
	motors.go_forward(m)
	time.sleep(1)
	motors.turn_left(m, math.pi/2, 1)
	time.sleep(2)
	motors.stop(m)
	return True


funcDict = {
    "tools.direct_kinematics()" : testKinematics,
    "motors.turn_left()": testTurnLeft
}

#Eventuellement ajouter un message en cas d'erreur ?
print("------ Testing begins ------")
for name, func in funcDict.items():
    print()
    print(Fore.WHITE + "Testing " + name + " ...")
    if func():
        print(Fore.GREEN + name + " successful.")
    else:
        print(Fore.RED + name + " unsuccessful.")
print()
print(Fore.WHITE + "------ End of testing ------")
