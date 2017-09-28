#########################################################################
# Header - Bibliotecas de Phidgets necesarias
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

#########################################################################
# Event Managers Definitions
#########################################################################

t = []
ac0 = []
ac1 = []
ac2 = []

try:
    ch = Accelerometer()
except RuntimeError as e:
    print("Runtime Exception %s" % e.details)
    print("Press Enter to Exit...\n")
    readin = sys.stdin.read(1)
    exit(1)

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
	print("\n")
	print("Aceleracion(gravedades) [x,y,z]: %f  %f  %f" % (acceleration[0], acceleration[1], acceleration[2]))
	print("Aceleracion(m/s^2) [x,y,z]: %f  %f  %f" % (acceleration[0]*9.80665, acceleration[1]*9.80665, acceleration[2]*9.80665))
	print("Timestamp: %f\n" % timestamp)
	t.append(timestamp)
	ac0.append(acceleration[0])
	ac1.append(acceleration[1])
	ac2.append(acceleration[2])

#########################################################################
# Programa Principal
#########################################################################

try:
	ch.setOnAttachHandler(AccelerometerAttached)
	ch.setOnDetachHandler(AccelerometerDetached)
	ch.setOnErrorHandler(ErrorEvent)
	ch.setOnAccelerationChangeHandler(AccelerationChangeHandler)

	print("Waiting for the Phidget Accelerometer Object to be attached...")
	ch.openWaitForAttachment(5000)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Press Enter to Exit...\n")
    readin = sys.stdin.read(1)
    exit(1)

# Definir el tiempo de muestro del acelerometro (En ms)

T_muestreo = 50 # 20 mediciones por segundo
ch.setDataInterval(T_muestreo)

# Esperar 5 segundos por las interrupciones del acelerometro

time.sleep(5)

# Cerrar el acelerometro
try:
    ch.close()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Press Enter to Exit...\n")
    readin = sys.stdin.read(1)
    exit(1)
print("Closed Accelerometer device")

# Graficar las aceleraciones en los tres ejes

ac0_np = np.array(ac0)#*9.80665
ac1_np = np.array(ac1)#*9.80665
ac2_np = np.array(ac2)#*9.80665
t_seg =  np.array(t)/1000

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


print("Tiempo de muestreo: " + str(T_muestreo) + " ms")
print("Mediciones Hechas: " +  str(len(ac0)))


plt.show()

Acceleration_Matrix = np.column_stack((ac0_np, ac1_np, ac2_np))
print("*********************************************")
print("Matriz de Aceleraciones:")
print("*********************************************")
print(Acceleration_Matrix)
Deviation_Matrix = Acceleration_Matrix - np.ones((len(ac0),3))*Acceleration_Matrix*(1/len(ac0))
print("*********************************************")
print("Matriz de Desviaciones:")
print("*********************************************")
print(Deviation_Matrix)
Covariance_Matrix = np.dot(Deviation_Matrix.transpose(),Deviation_Matrix)
print("*********************************************")
print("Matriz de Covarianza:")
print("*********************************************")
print(Covariance_Matrix)

# Transformadas de Fourier de las senales
#fft_ac0 = np.fft.fft(ac0_np)
#freq = np.fft.fftfreq(t_seg.shape[-1])
#plt.plot(freq, fft_ac0.real)
#plt.title('Fourier Ac0')
#plt.xlabel('Frequencia (Hz)')
#plt.ylabel('Amplitud')
#plt.grid(True)
#plt.show()

exit(0)
