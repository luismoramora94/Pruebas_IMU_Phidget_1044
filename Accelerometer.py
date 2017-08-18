import sys
import time
import numpy as np
import matplotlib.pyplot as plt
 
from Phidget22.Devices.Accelerometer import *
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Net import *


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
    print("Aceleracion(gravedades) [x,y,z]: %f  %f  %f" % (acceleration[0], acceleration[1], acceleration[2]))
    print("Aceleracion(m/s^2) [x,y,z]: %f  %f  %f" % (acceleration[0]*9.80665, acceleration[1]*9.80665, acceleration[2]*9.80665))
    print("Timestamp: %f\n" % timestamp)
    t.append(timestamp) 
    ac0.append(acceleration[0]) 
    ac1.append(acceleration[1])
    ac2.append(acceleration[2])
   # np.insert(t,timestamp)
   # np.insert(ac,acceleration[0])
try:
    ch.setOnAttachHandler(AccelerometerAttached)
    ch.setOnDetachHandler(AccelerometerDetached)
    ch.setOnErrorHandler(ErrorEvent)

    ch.setOnAccelerationChangeHandler(AccelerationChangeHandler)

    # Please review the Phidget22 channel matching documentation for details on the device
    # and class architecture of Phidget22, and how channels are matched to device features.

    # Specifies the serial number of the device to attach to.
    # For VINT devices, this is the hub serial number.
    #
    # The default is any device.
    #
    # ch.setDeviceSerialNumber(<YOUR DEVICE SERIAL NUMBER>) 

    # For VINT devices, this specifies the port the VINT device must be plugged into.
    #
    # The default is any port.
    #
    # ch.setHubPort(0)

    # Specifies that the channel should only match a VINT hub port.
    # The only valid channel id is 0.
    #
    # The default is 0 (false), meaning VINT hub ports will never match
    #
    # ch.setIsHubPortDevice(1)

    # Specifies which channel to attach to.  It is important that the channel of
    # the device is the same class as the channel that is being opened.
    #
    # The default is any channel.
    #
    # ch.setChannel(0)

    # In order to attach to a network Phidget, the program must connect to a Phidget22 Network Server.
    # In a normal environment this can be done automatically by enabling server discovery, which
    # will cause the client to discovery and connect to available servers.
    #
    # To force the channel to only match a network Phidget, set remote to 1.
    #
    # Net.enableServerDiscovery(PhidgetServerType.PHIDGETSERVER_DEVICE);
    # ch.setIsRemote(1)

    print("Waiting for the Phidget Accelerometer Object to be attached...")
    ch.openWaitForAttachment(5000)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Press Enter to Exit...\n")
    readin = sys.stdin.read(1)
    exit(1)

print("Muestreando Aceleraciones por 5 segundos...")
time.sleep(5)


try:
    ch.close()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Press Enter to Exit...\n")
    readin = sys.stdin.read(1)
    exit(1) 
print("Closed Accelerometer device")

# Graficar las aceleraciones en los tres ejes 

#plt.plot(t,ac0)
#plt.show()
#plt.plot(t,ac1)
#plt.show()
#plt.plot(t,ac2)
#plt.show()

# Obtener valor promedio de las aceleraciones

ac0_np = np.array(ac0)
ac1_np = np.array(ac1)
ac2_np = np.array(ac2)

print("Valor Promedio de la aceleracion X: %f g \n" % ( np.mean(ac0_np)))
print("Valor Promedio de la aceleracion X: %f m/s^2 \n" % (9.80665*np.mean(ac0_np)))

print("Valor Promedio de la aceleracion Y: %f g \n" % ( np.mean(ac1_np)))
print("Valor Promedio de la aceleracion Y: %f m/s^2 \n" % (9.80665*np.mean(ac1_np)))

print("Valor Promedio de la aceleracion Z: %f g \n" % ( np.mean(ac2_np)))
print("Valor Promedio de la aceleracion Z: %f m/s^2 \n" % (9.80665*np.mean(ac2_np)))

exit(0)
                     
