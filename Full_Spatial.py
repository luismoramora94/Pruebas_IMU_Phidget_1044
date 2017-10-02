#########################################################################
# Header - Bibliotecas de Numpy, matplotlib y Phidgets necesarias
#########################################################################

import sys
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from Phidget22.Devices.Spatial import *
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Net import *

#########################################################################
# Event Manager Definitions
#########################################################################

tiempo = []
ac0 = []
ac1 = []
ac2 = []
gr0 = []
gr1 = []
gr2 = []
mg0 = []
mg1 = []
mg2 = []

try:
	Space = Spatial()

except RuntimeError as e:
    print("Runtime Exception %s" % e.details)
    print("Press Enter to Exit...\n")
    readin = sys.stdin.read(1)
    exit(1)

########################### Spatial Setup
def SpatialAttached(e):
    try:
        attached = e
        print("\nAttach Event Detected (Information Below)")
        print("===========================================")
        print("Library Version: %s" % attached.getLibraryVersion())
        print("Serial Number: %d" % attached.getDeviceSerialNumber())
        print("Channel: %d" % attached.getChannel())
        print("Channel Class: %s" % attached.getChannelClass())
        print("Channel Name: %s" % attached.getChannelName())
        print("Device ID: %d" % attached.getDeviceID())
        print("Device Version: %d" % attached.getDeviceVersion())
        print("Device Name: %s" % attached.getDeviceName())
        print("Device Class: %d" % attached.getDeviceClass())
        print("\n")

    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Press Enter to Exit...\n")
        readin = sys.stdin.read(1)
        exit(1)

def SpatialAttached(e):
	    try:
	        attached = e
	        print("\nAttach Event Detected (Information Below)")
	        print("===========================================")
	        print("Library Version: %s" % attached.getLibraryVersion())
	        print("Serial Number: %d" % attached.getDeviceSerialNumber())
	        print("Channel: %d" % attached.getChannel())
	        print("Channel Class: %s" % attached.getChannelClass())
	        print("Channel Name: %s" % attached.getChannelName())
	        print("Device ID: %d" % attached.getDeviceID())
	        print("Device Version: %d" % attached.getDeviceVersion())
	        print("Device Name: %s" % attached.getDeviceName())
	        print("Device Class: %d" % attached.getDeviceClass())
	        print("\n")

	    except PhidgetException as e:
	        print("Phidget Exception %i: %s" % (e.code, e.details))
	        print("Press Enter to Exit...\n")
	        readin = sys.stdin.read(1)
	        exit(1)

def SpatialDetached(e):
    detached = e
    try:
        print("\nDetach event on Port %d Channel %d" % (detached.getHubPort(), detached.getChannel()))
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Press Enter to Exit...\n")
        readin = sys.stdin.read(1)
        exit(1)

def ErrorEvent(e, eCode, description):
    print("Error %i : %s" % (eCode, description))

def SpatialDataHandler(e, acceleration, angularRate, fieldStrength, timestamp):
	tiempo.append(timestamp)
	ac0.append(acceleration[0])
	ac1.append(acceleration[1])
	ac2.append(acceleration[2])
	gr0.append(angularRate[0])
	gr1.append(angularRate[1])
	gr2.append(angularRate[2])
	mg0.append(fieldStrength[0])
	mg1.append(fieldStrength[1])
	mg2.append(fieldStrength[2])

# Programa Principal
#########################################################################

try:
	Space.setOnAttachHandler(SpatialAttached)
	Space.setOnDetachHandler(SpatialDetached)
	Space.setOnErrorHandler(ErrorEvent)
	Space.setOnSpatialDataHandler(SpatialDataHandler)
	#########################################################################
	print("Waiting for the Phidget Spatial Object to be attached...")
	Space.openWaitForAttachment(5000)
	print("Spatial attached")
	#########################################################################
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Press Enter to Exit...\n")
    readin = sys.stdin.read(1)
    exit(1)

# Definir el tiempo de muestro del acelerometro (En ms)

T_muestreo = 50 # 20 mediciones por segundo
Space.setDataInterval(T_muestreo)

# Muestrear 5 segundos
time.sleep(5)

try:
    Space.close()

except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Press Enter to Exit...\n")
    readin = sys.stdin.read(1)
    exit(1)
print("Closed Spatial Device")

# Convetir los vectores a arreglos de numpy para hacer los calculos mas eficientes

ac0_np = np.array(ac0)#*9.80665
ac1_np = np.array(ac1)#*9.80665
ac2_np = np.array(ac2)#*9.80665
t_seg =  np.array(tiempo)/1000

gr0_np = np.array(gr0)
gr1_np = np.array(gr1)
gr2_np = np.array(gr2)


mg0_np = np.array(mg0)
mg1_np = np.array(mg1)
mg2_np = np.array(mg2)


# Graficas de Aceleracion

plt.figure(1)
plt.subplot(221)
plt.plot(t_seg,ac0_np)
plt.title('Aceleracion en X')
plt.xlabel('Tiempo (s)')
plt.ylabel('Aceleracion (m/s^2)')
plt.grid(True)

plt.subplot(222)
plt.plot(t_seg,ac1_np)
plt.title('Aceleracion en Y')
plt.xlabel('Tiempo (s)')
plt.ylabel('Aceleracion (m/s^2)')
plt.grid(True)

plt.subplot(223)
plt.plot(t_seg,ac2_np)
plt.title('Aceleracion en Z')
plt.xlabel('Tiempo (s)')
plt.ylabel('Aceleracion (m/s^2)')
plt.grid(True)

plt.subplots_adjust(top=0.92, bottom=0.1, left=0.15, right=0.95, hspace=0.5, wspace=0.7)

# Obtener valores promedio de las aceleraciones

#print("Valor Promedio de la aceleracion en X: %f g \n" % ( np.mean(ac0_np)))
print("Valor Promedio de la aceleracion en X: %f m/s^2 \n" % (np.mean(ac0_np)))

#print("Valor Promedio de la aceleracion en Y: %f g \n" % ( np.mean(ac1_np)))
print("Valor Promedio de la aceleracion en Y: %f m/s^2 \n" % (np.mean(ac1_np)))

#print("Valor Promedio de la aceleracion en Z: %f g \n" % ( np.mean(ac2_np)))
print("Valor Promedio de la aceleracion en Z: %f m/s^2 \n" % (np.mean(ac2_np)))

plt.show()


# Graficas del giroscopio

plt.figure(2)
plt.subplot(221)
plt.plot(t_seg,gr0_np)
plt.title('Velocidad Angular en X')
plt.xlabel('Tiempo (s)')
plt.ylabel('Velocidad (rad/s)')
plt.grid(True)

plt.subplot(222)
plt.plot(t_seg,gr1_np)
plt.title('Velocidad Angular en Y')
plt.xlabel('Tiempo (s)')
plt.ylabel('Velocidad Angular (rad/s)')
plt.grid(True)

plt.subplot(223)
plt.plot(t_seg,gr2_np)
plt.title('Velocidad Angular en Z')
plt.xlabel('Tiempo (s)')
plt.ylabel('Velocidad (rad/s)')
plt.grid(True)

plt.subplots_adjust(top=0.92, bottom=0.1, left=0.15, right=0.95, hspace=0.5, wspace=0.7)

# Obtener valores promedio de las velocidades angulares


print("Valor Promedio de la velocidad angular en X: %f rad/s \n" % (np.mean(gr0_np)))


print("Valor Promedio de la velocidad angular en Y: %f rad/s \n" % (np.mean(gr1_np)))


print("Valor Promedio de la velocidad angular en Z: %f rad/s \n" % (np.mean(gr2_np)))

plt.show()

# Graficas del magnetometro

plt.figure(3)
plt.subplot(221)
plt.plot(t_seg,mg0_np)
plt.title('Campo Magnetico en X')
plt.xlabel('Tiempo (s)')
plt.ylabel('Intensidad (G)')
plt.grid(True)

plt.subplot(222)
plt.plot(t_seg,mg1_np)
plt.title('Campo Magnetico en Y')
plt.xlabel('Tiempo (s)')
plt.ylabel('Intensidad (G)')
plt.grid(True)

plt.subplot(223)
plt.plot(t_seg,mg2_np)
plt.title('Campo Magnetico en Z')
plt.xlabel('Tiempo (s)')
plt.ylabel('Intensidad (G)')
plt.grid(True)

plt.subplots_adjust(top=0.96, bottom=0.1, left=0.15, right=0.95, hspace=0.5, wspace=0.7)

# Obtener valores promedio de las velocidades angulares


print("Valor Promedio de la intensidad de campo magnetico en X: %f mG \n" % (np.mean(mg0_np)))


print("Valor Promedio de la intensidad de campo magnetico en Y: %f mG \n" % (np.mean(mg1_np)))


print("Valor Promedio de la intensidad de campo magnetico en Z: %f mG \n" % (np.mean(mg2_np)))


print("Tiempo de muestreo: " + str(T_muestreo) + " ms")
print("Mediciones Hechas: " +  str(len(mg0)))

plt.show()

### Matrices de Covarianza

# Acelerometro

Acceleration_Matrix = np.column_stack((ac0_np, ac1_np, ac2_np))
Deviation_Matrix = Acceleration_Matrix - np.ones((len(ac0),3))*Acceleration_Matrix*(1/len(ac0))
Covariance_Matrix = np.dot(Deviation_Matrix.transpose(),Deviation_Matrix)
print("******************************************************")
print("Matriz de Covarianza de Aceleracion:")
print("******************************************************")
print(Covariance_Matrix)

# Giroscopio

Angular_Rate_Matrix = np.column_stack((gr0_np, gr1_np, gr2_np))
Angular_Rate_Deviation_Matrix = Angular_Rate_Matrix - np.ones((len(gr0),3))*Angular_Rate_Matrix*(1/len(gr0))
Angular_Rate_Covariance_Matrix = np.dot(Angular_Rate_Deviation_Matrix.transpose(),Angular_Rate_Deviation_Matrix)
print("******************************************************")
print("Matriz de Covarianza de Velocidades Angulares:")
print("******************************************************")
print(Angular_Rate_Covariance_Matrix)

# Magnetometro

Magneto_Matrix = np.column_stack((mg0_np, mg1_np, mg2_np))
Magneto_Deviation_Matrix = Magneto_Matrix - np.ones((len(mg0),3))*Magneto_Matrix*(1/len(mg0))
Magneto_Covariance_Matrix = np.dot(Magneto_Deviation_Matrix.transpose(),Magneto_Deviation_Matrix)

print("******************************************************")
print("Matriz de Covarianza de Campo Magnetico:")
print("******************************************************")
print(Magneto_Covariance_Matrix)


# Magnetometro,  giroscopio Y acelerometro

Full_Matrix = np.column_stack((ac0_np, ac1_np, ac2_np,gr0_np, gr1_np, gr2_np, mg0_np, mg1_np, mg2_np))
Full_Deviation_Matrix = Full_Matrix - np.ones((len(gr0),9))*Full_Matrix*(1/len(gr0))
Full_Covariance_Matrix = np.dot(Full_Deviation_Matrix.transpose(),Full_Deviation_Matrix)
print("******************************************************************************")
print("Matriz de Covarianza de aceleracion y velocidad angular y campo magnetico:")
print("******************************************************************************")
print(Full_Covariance_Matrix)

exit(0)
