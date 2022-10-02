# IMPORT ALL MODULES
import math
import pandas as pd


# Define all car characteristics
VERSIONNUMBER = 1.1









# OLD CODE
# def motor_torque(drivingRPM):
#     return 120
#     #120  # Peak torque supplied by the motor; peak, non-continuous: 230 (Nm)
#     # if drivingRPM < 5500
#
#
# def calc_motor_top_speed(gearRatio):  # Top speed limited by motor
#     # Output: m/s
#     return MOTORMAXRPM / gearRatio * 2 * math.pi * tireRadius / 60
#
#
# def calc_acceleration(velocity, gearRatio):
#     # Input: m/s; Output: m/s^2
#     drivenRPM = velocity / (2 * math.pi * tireRadius) * 60
#     drivingRPM = 0
#     return ((((motor_torque(drivingRPM) - DRIVINGRESISTANCE) * gearRatio - DRIVENRESISTANCE) / (4 * (DRIVENINERTIA / pow(gearRatio, 2) + DRIVINGINERTIA)) * tireRadius) * 4 * TIREMASS - (4 * RESISTIVECOEFFICIENT * (CARMASS * GRAVITY + LIFTCOEFFICIENT * AREA * pow(velocity, 2) * AIRDENSITY / 2) + DRAGCOEFFICIENT * AREA * pow(velocity, 2) * AIRDENSITY / 2)) / CARMASS
#
#
# def calc_velocity(initialVelocity, gearRatio):
#     stepCount = 10000
#     totalTime = 20
#     currentVelocity = initialVelocity
#     global timeLst
#     global velocityLst
#     global kmhrLst
#     i = 0
#     timeLst = []
#     velocityLst = []
#     kmhrLst = []
#     while(i < stepCount):
#         timeLst.append(totalTime * i / stepCount)
#         currentVelocity = currentVelocity + calc_acceleration(currentVelocity, gearRatio) * totalTime / stepCount
#         velocityLst.append(currentVelocity)
#         kmhrLst.append(currentVelocity * 3.6)
#         i += 1
#         if round(calc_acceleration(currentVelocity, gearRatio), 1) == 0: break
#     return velocityLst[i - 1]
#
#
# def graph_velocity(gearRatio):
#     global aeroTopSpeed
#     aeroTopSpeed = calc_velocity(0, gearRatio)
#     df = pd.DataFrame({'Time Elapsed (s)': timeLst, 'Velocity (km/hr)':kmhrLst})
#     writer = pd.ExcelWriter(str(gearRatio) + " reduction velocity curve.xlsx", engine='xlsxwriter')
#     df.to_excel(writer, sheet_name='Data')
#     writer.save()
#
#
# graph_velocity(GEARDEFAULT)
# print('Gear Ratio: ' + str(GEARDEFAULT))
# print('Acceleration (g): ' + str(calc_acceleration(0,GEARDEFAULT) / GRAVITY)) # Expected <= 1g (around 0.4 for IC); ABS Max 1.6-1.9
# print('Inertia Ratio: ' + str(DRIVENINERTIA / DRIVINGINERTIA))
# print('Motor Top Speed (km/hr): ' + str(calc_motor_top_speed(GEARDEFAULT) * 3.6))
# print('Aero Top Speed (km/hr): ' + str(aeroTopSpeed * 3.6))



# Future additions / improvements
# Ti grip = ~ 240 lb (per tire)
# Figure out  Cl and Cd values (current ones are from before cutout design)
# Incline angle
# Current theory might be incorrect (torque conversion to acceleration)
# Accumulator Limitations
# Look into Driven/Driving Inertia (sprocket is technically part of driving?)
# Have accel. specific values - for Drag & Lift
# - 2 & 1.1 (according to sims)
# ~ 1.35 & 0.705 (according to nick) "At 20 mph we were at Cl*A=3.22 and Cd*A=1.57, and once we got to 50 mph we were at Cl*A=2.84 and Cd*A=1.35"
# 0-60 time
# Get better data
# Chain Stretch (inc tensioner)
# Changing Tire Radius
# Tire max grip
# Motor RPM limit (and torque fall-off)
# - find the closest value within 1 mph to 60 mph; output time
# Accel
# (Skidpad)
# (Endurance)
# (Efficiency)
# Clean up excel files
# Torque curve
# Variable names
# Json capability
# Modernization (similar to lapsim model
