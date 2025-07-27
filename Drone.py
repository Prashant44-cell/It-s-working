
import scipy as sp
from dronekit import connect, VehicleMode, LocationGlobalRelative, Command
from pymavlink import mavutil
import time


# Connect to the vehicle
print("Connecting to vehicle...")
vehicle = connect("tcp:127.0.0.1:5762", wait_ready=True, timeout=60)

# Wait until vehicle is armable
while not vehicle.is_armable:
    print("Waiting for vehicle to become armable...")
    time.sleep(1)

# Set mode to GUIDED
vehicle.mode = VehicleMode("GUIDED")
while vehicle.mode.name != "GUIDED":
    print("Waiting for GUIDED mode...")
    time.sleep(1)

# Arm the vehicle
vehicle.armed = True
while not vehicle.armed:
    print("Waiting for arming...")
    time.sleep(1)
print("Vehicle armed.")

# Takeoff
target_altitude = 20
print(f"Taking off to {target_altitude} meters...")
vehicle.simple_takeoff(target_altitude)
while True:
    current_alt = vehicle.location.global_relative_frame.alt
    print(f"Altitude: {current_alt:.2f}")
    if current_alt >= target_altitude * 0.95:
        print("Reached target altitude.")
        break
    time.sleep(10)
    target_location = LocationGlobalRelative(12.9724723, 80.0427222,20)  
   
    vehicle.simple_goto(target_location)
    time.sleep(5)
    subprocess["python","Survilence.py"]


# Switch to ALT_HOLD
print("Switching to ALT_HOLD...")
vehicle.mode = VehicleMode("ALT_HOLD")
time.sleep(2)

#  Hover for 5 seconds
print("Hovering in place for image capture...")
time.sleep(5)

def send_ned_velocity(vx, vy, vz, duration):
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,
        0,
        0,
        mavutil.mavlink.MAV_FRAME_LOCAL_NED,
        0b0000111111000111,
        100,
        0,
        0,
        vx,
        vy,
        vz,
        100,
        5,
        0,
        0,
        0,
    )
    for _ in range(duration):
        vehicle.send_mavlink(msg)
        time.sleep(1)
    

# Its a direction given in x,y and z dirextion along with duration
send_ned_velocity(100, -5, -10, 5)

send_ned_velocity(100, -5, 10, 5)

# vehicle.mode = VehicleMode("LOITER")


# Return to Launch
print("Commanding Return to Launch...")
vehicle.mode = VehicleMode("RTL")

#close the vehicle
time.sleep(10)
print("Closing vehicle connection.")
vehicle.close()
