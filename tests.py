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
	m.rotate_two_wheels(math.pi/2)
	return True

def testTurnRight():
	m = motors.Motors()
	m.rotate_two_wheels(-math.pi/2)
	return True

funcDict = {
    "tools.direct_kinematics()" : testKinematics,
    "motors.rotate_two_wheels(math.pi/4)": testTurnLeft,
    "motors.rotate_two_wheels(-math.pi/4)": testTurnRight
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


#### Test unitaire ####

def testOdom(v_gauche_motor, v_droit_motor):
    
    x_dot, theta_dot = direct_kinematics(v_gauche_motor, v_droit_motor)

    x, y, theta, t_n_1 = tick_odom( 0, 0, 0, 0, x_dot, theta_dot, 1)
    
    print("v_gauche_motor =", v_gauche_motor)
    print("v_droit_motor =", v_droit_motor)
    print("x =", x)
    print("y =", y)
    print("theta =", theta)
    print("t_n_1 =", t_n_1)

def  testVitesseAngulaire(motor, vitesse_angulaire):
    #motor = l'identifiant du moteur testé
    #vitesse_angulire = vitesse angulaire testé.
    
    #à poser sur le scotch, ouis on regarde le nombre de tour que la roue effectue.
    print("La roue devrait tourner", vitesse_angulaire * 5 / 360, "fois")
    m = motors.Motors()
    m.DXL_IO.set_moving_speed({motor: vitesse_angulaire})
    
    time.sleep(5000)
    
    m.DXL_IO.set_moving_speed({motor: 0})
    
def testVitesseTraitement():
    t = time.time()
    m = motors.Motors()
    m.go_forward()
    
    verif_v_gauche, verif_v_droit = m.get_current_speed_wheels()
    print("Vitesse de la roue gauche :", verif_v_gauche)
    print("Vitesse de la roue droite :", verif_v_droit)
    
    input("appuyer quand le robot bouge")
    print("Le temps de réponse est :", round(time.time() - t, 3), "s")
    
    t = time.time()
    m.turn_right(math.pi, 4)
    verif_v_gauche, verif_v_droit = m.get_current_speed_wheels()
    print("Vitesse de la roue gauche :", verif_v_gauche)
    print("Vitesse de la roue droite :", verif_v_droit)
    
    input("appuyer quand le robot bouge")
    print("Le temps de réponse est :", round(time.time() - t, 3), "s")
    