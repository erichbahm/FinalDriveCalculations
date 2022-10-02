# IMPORT ALL MODULES
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot
from scipy.integrate import quad


# DEFINE ALL PHYSICAL CAR CHARACTERISTICS
GRAVITY = 9.80665 # Gravitational acceleration (m/s^2)
CARWEIGHT = 2668.93 # Total EXPECTED weight of all components in the car including the driver (N)
CARMASS = CARWEIGHT / GRAVITY # Total EXPECTED mass of all components in the car including the driver (kg)
MOTORTORQUE = 120 # Peak torque supplied by the motor; peak, non-continuous: 230 (Nm)
AREA = 1 # Front facing AREA of the car (m^2)
INCLINEANGLE = 0 # Incline angle of the road (rad)
AIRDENSITY = 1.2754 # Density of air during given conditions (kg/m^3)
DRAGCOEFFICIENT = 0#1.41 # Coefficient of Drag - Cd
LIFTCOEFFICIENT = 0#2.77 # Coefficient of lift - Cl
RESISTIVECOEFFICIENT = 0.015 # Coefficient of rolling resistance of each tire
MOTORINERTIA = 0.0383 # Moment of inertia of the motor (kgm^2)
LOADINERTIA = 0.15 # Moment of inertia of all moving components (kgm^2)
INTERNALFRICTION = 0.012 * MOTORTORQUE # Internal friction of rotating components in terms of torque (Nm)
tireRadius = 0.2032 # Tread radius of each tire (m)
ztsRatio = []
ztsTime = []


# DEFINE EQUATIONS AS FUNCTIONS
def calc_accel_time(initialVelocity, finalVelocity, gearRatio): # Velocity units m/s
    finalRPM = 60 * finalVelocity / (2 * math.pi * tireRadius / gearRatio) # RPM
    initialRPM = 60 * initialVelocity / (2 * math.pi * tireRadius * gearRatio) # RPM
    print('Top Part: ' + str(- ((LOADINERTIA * pow(gearRatio,2) + MOTORINERTIA) + pow(gearRatio, 2) * pow(tireRadius, 2) * CARMASS)))
    print('Coefficient: ' + str((gearRatio * tireRadius * (DRAGCOEFFICIENT * AIRDENSITY * AREA / 2 * pow(2 * math.pi * tireRadius * gearRatio, 2) + 4 * RESISTIVECOEFFICIENT * (CARWEIGHT * math.cos(INCLINEANGLE) + LIFTCOEFFICIENT * AIRDENSITY * AREA / 2 * pow(2 * math.pi * tireRadius * gearRatio, 2))))))
    print('Bottom Part: ' + str(CARWEIGHT * math.sin(INCLINEANGLE) + INTERNALFRICTION - MOTORTORQUE))
    return quad(lambda RPM: - ((LOADINERTIA * pow(gearRatio,2) + MOTORINERTIA) + pow(gearRatio, 2) * pow(tireRadius, 2) * CARMASS) / (gearRatio * tireRadius * (DRAGCOEFFICIENT * AIRDENSITY * AREA / 2 * pow(2 * math.pi * tireRadius * gearRatio * RPM, 2) + 4 * RESISTIVECOEFFICIENT * (CARWEIGHT * math.cos(INCLINEANGLE) + LIFTCOEFFICIENT * AIRDENSITY * AREA / 2 * pow(2 * math.pi * tireRadius * gearRatio * RPM, 2)) + CARWEIGHT * math.sin(INCLINEANGLE)) + INTERNALFRICTION - MOTORTORQUE), initialRPM, finalRPM)[0]


def calc_zts(gearLB, gearUB):
    pointCount = 10000
    for i in range(pointCount):
        ztsRatio.append(gearLB + (gearUB - gearLB) / pointCount * i)
        ztsTime.append(calc_accel_time(0, 88, gearLB + (gearUB - gearLB) / pointCount * i))
    create_xlsx({"Gear Ratio":ztsRatio,"ZTS Time":ztsTime},'Zero_to_Sixty_Time.xlsx')

def create_xlsx(titleDict, xlsxName):
    df = pd.DataFrame(titleDict)
    writer = pd.ExcelWriter(xlsxName, engine='xlsxwriter')
    df.to_excel(writer, sheet_name="Sheet1")
    writer.save()

def calc_test(initialVelocity, finalVelocity, gearRatio):
    pointCount = 1000
    for i in range(pointCount):
        ztsRatio.append(finalVelocity * i / pointCount)
        ztsTime.append(calc_accel_time(initialVelocity, (finalVelocity-initialVelocity) * i / 1000 + initialVelocity, gearRatio))
    create_xlsx({"Gear Ratio":ztsRatio,"ZTS Time":ztsTime},'Zero_to_Sixty_Time.xlsx')

def calc_top_speed(gearRatio):
    return 5500 / gearRatio * 2 * math.pi * tireRadius * 60 / 1000

def graph_top_speed(gearLB, gearUB, steps):
    topSpeed = []
    tsGear = []
    for i in range(steps):
        geari = gearLB + (gearUB - gearLB) / (steps - 1) * i
        tsGear.append(geari)
        topSpeed.append(calc_top_speed(geari))
    create_xlsx({'Gear Ratio':tsGear, "Top Speed":topSpeed},'Top_speed.xlsx')

print(calc_accel_time(0, 20, 1/3.5))
# calc_zts(3,7)
# calc_test(0,14.0154,3.5)
# graph_top_speed(1, 7, 1000)