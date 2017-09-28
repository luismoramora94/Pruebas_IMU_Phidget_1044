#########################################################################
# Header - Bibliotecas de Numpy, matplotlib y Phidgets necesarias
#########################################################################

import sys
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from Phidget22.Devices.Accelerometer import *
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Net import *
from Phidget22.Devices.Gyroscope import *

#########################################################################
# Event Manager Definitions
#########################################################################

t = []
t_gyro = []
ac0 = []
ac1 = []
ac2 = []
gr0 = []
gr1 = []
gr2 = []

try:
    ch = Accelerometer()
    Gyro = Gyroscope()
except RuntimeError as e:
    print("Runtime Exception %s" % e.details)
    print("Press Enter to Exit...\n")
    readin = sys.stdin.read(1)
    exit(1)
########################### Accelerometer Setup
def AccelerometerAttached(e):
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

def AccelerometerDetached(e):
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

def AccelerationChangeHandler(e, acceleration, timestamp):
	#print("\n")
	#print("Aceleracion(gravedades) [x,y,z]: %f  %f  %f" % (acceleration[0], acceleration[1], acceleration[2]))
	#print("Aceleracion(m/s^2) [x,y,z]: %f  %f  %f" % (acceleration[0]*9.80665, acceleration[1]*9.80665, acceleration[2]*9.80665))
	#print("Timestamp: %f\n" % timestamp)
	t.append(timestamp)
	ac0.append(acceleration[0])
	ac1.append(acceleration[1])
	ac2.append(acceleration[2])

########################### Gyroscope Setup

def GyroscopeAttached(gr):
    try:
        g_attached = gr
        print("\nAttach Event Detected (Information Below)")
        print("===========================================")
        print("Library Version: %s" % g_attached.getLibraryVersion())
        print("Serial Number: %d" % g_attached.getDeviceSerialNumber())
        print("Channel: %d" % g_attached.getChannel())
        print("Channel Class: %s" % g_attached.getChannelClass())
        print("Channel Name: %s" % g_attached.getChannelName())
        print("Device ID: %d" % g_attached.getDeviceID())
        print("Device Version: %d" % g_attached.getDeviceVersion())
        print("Device Name: %s" % g_attached.getDeviceName())
        print("Device Class: %d" % g_attached.getDeviceClass())
        print("\n")

    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Press Enter to Exit...\n")
        readin = sys.stdin.read(1)
        exit(1)
def GyroscopeDetached(e):
    detached = e
    try:
        print("\nDetach event on Port %d Channel %d" % (detached.getHubPort(), detached.getChannel()))
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Press Enter to Exit...\n")
        readin = sys.stdin.read(1)
        exit(1)

def AngularRateUpdateHandler(e, angularRate, timestamp):
    #print("Angular Rate: %f  %f  %f" % (angularRate[0], angularRate[1], angularRate[2]))
    #print("Timestamp: %f\n" % timestamp)
    t_gyro.append(timestamp)
    gr0.append(angularRate[0])
    gr1.append(angularRate[1])
    gr2.append(angularRate[2])

# Programa Principal
#########################################################################

try:
	ch.setOnAttachHandler(AccelerometerAttached)
	ch.setOnDetachHandler(AccelerometerDetached)
	ch.setOnErrorHandler(ErrorEvent)
	ch.setOnAccelerationChangeHandler(AccelerationChangeHandler)

	#########################################################################
	print("Waiting for the Phidget Accelerometer Object to be attached...")
	ch.openWaitForAttachment(5000)
	print("Accelerometer attached")
	Gyro.setOnAttachHandler(GyroscopeAttached)
	Gyro.setOnDetachHandler(GyroscopeDetached)
	Gyro.setOnErrorHandler(ErrorEvent)
	Gyro.setOnAngularRateUpdateHandler(AngularRateUpdateHandler)

	print("Waiting for the Phidget Gyroscope Object to be attached...")
	Gyro.openWaitForAttachment(5000)
	print("Gyroscope attached")

except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Press Enter to Exit...\n")
    readin = sys.stdin.read(1)
    exit(1)

# Definir el tiempo de muestro del acelerometro (En ms)

T_muestreo = 50 # 20 mediciones por segundo
ch.setDataInterval(T_muestreo)
Gyro.setDataInterval(T_muestreo)

# Muestrear 5 segundos el acelerometro y giroscopio

time.sleep(5)

# Cerrar el acelerometro y giroscopio
# Finaliza muestreo de datos
try:
    ch.close()
    Gyro.close()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Press Enter to Exit...\n")
    readin = sys.stdin.read(1)
    exit(1)
print("Closed Accelerometer device")
print("Closed Gyroscope device")

# Convetir los vectores a arreglos de numpy para hacer los calculos mas eficientes

ac0_np = np.array(ac0)#*9.80665
ac1_np = np.array(ac1)#*9.80665
ac2_np = np.array(ac2)#*9.80665
t_seg =  np.array(t)/1000

gr0_np = np.array(gr0)
gr1_np = np.array(gr1)
gr2_np = np.array(gr2)
t_gyro_seg =  np.array(t_gyro)/1000

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

print("Mediciones de Aceleracion Hechas: " +  str(len(ac0)))

plt.show()


# Graficas del giroscopio

plt.figure(2)
plt.subplot(221)
plt.plot(t_gyro_seg,gr0_np)
plt.title('Velocidad Angular en X')
plt.xlabel('Tiempo (s)')
plt.ylabel('Velocidad (rad/s)')
plt.grid(True)

plt.subplot(222)
plt.plot(t_gyro_seg,gr1_np)
plt.title('Velocidad Angular en Y')
plt.xlabel('Tiempo (s)')
plt.ylabel('Velocidad Angular (rad/s)')
plt.grid(True)

plt.subplot(223)
plt.plot(t_gyro_seg,gr2_np)
plt.title('Velocidad Angular en Z')
plt.xlabel('Tiempo (s)')
plt.ylabel('Velocidad (rad/s)')
plt.grid(True)

plt.subplots_adjust(top=0.92, bottom=0.1, left=0.15, right=0.95, hspace=0.5, wspace=0.7)

# Obtener valores promedio de las velocidades angulares


print("Valor Promedio de la velocidad angular en X: %f rad/s \n" % (np.mean(gr0_np)))


print("Valor Promedio de la velocidad angular en Y: %f rad/s \n" % (np.mean(gr1_np)))


print("Valor Promedio de la velocidad angular en Z: %f rad/s \n" % (np.mean(gr2_np)))


print("Tiempo de muestreo: " + str(T_muestreo) + " ms")
print("Mediciones de Aceleracion Hechas: " +  str(len(gr0)))

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

# Giroscopio Y acelerometro

Angular_Rate_Accelerometer_Matrix = np.column_stack((ac0_np, ac1_np, ac2_np,gr0_np, gr1_np, gr2_np))
Angular_Rate_Accelerometer_Deviation_Matrix = Angular_Rate_Accelerometer_Matrix - np.ones((len(gr0),6))*Angular_Rate_Accelerometer_Matrix*(1/len(gr0))
Angular_Rate_Accelerometer_Covariance_Matrix = np.dot(Angular_Rate_Accelerometer_Deviation_Matrix.transpose(),Angular_Rate_Accelerometer_Deviation_Matrix)
print("******************************************************")
print("Matriz de Covarianza de Giroscopio y Acelerometro:")
print("******************************************************")
print(Angular_Rate_Accelerometer_Covariance_Matrix)

exit(0)
