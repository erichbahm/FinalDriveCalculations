# IMPORT ALL MODULES
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot
from scipy.integrate import quad


# DEFINE ALL PHYSICAL CAR CHARACTERISTICS
GRAVITY = 32.17405  # Gravitational acceleration (ft/s^2)
CARWEIGHT = 600  # Total weight of all components in the car including the driver (lb)
CARMASS = CARWEIGHT / GRAVITY  # Total mass of all components in the car including the driver - goal (slug)
MOTORTORQUE = 98.82  # Peak torque supplied by the motor; 40.5 is peak continuous (lbft)
AREA = 1  # Front facing AREA of the car (ft^2)
INCLINEANGLE = 0  # Incline angle of the road (rad)
AIRDENSITY = 0.00247468454  # Density of air during given conditions (slug/ft^3)
DRAGCOEFFICIENT = 15.17711  # Coefficient of Drag - Cd; 1.41 m^2
LIFTCOEFFICIENT = 29.81603  # Coefficient of lift - Cl; 2.77 m^2
RESISTIVECOEFFICIENT = 0.015  # Coefficient of rolling resistance of each tire
MOMENTINERTIA = 2.2781145988  # Reflect moment of inertia of all moving components - including the motor (slugft^2); 0.07080596624347686
INTERNALFRICTION = 0.5  # Internal friction of rotating components in terms of torque (lbft)
tireRadius = 16/12  # Tread to tread radius of each tire (ft)
ztsRatio = []
ztsTime = []


# DEFINE EQUATIONS AS FUNCTIONS
def quick_calc(initialVelocity, finalVelocity, gearRatio): # final velocity units ft/s
    finalRPM = 60 * finalVelocity / (2 * math.pi * tireRadius) # RPM
    initialRPM = 60 * initialVelocity / (2 * math.pi * tireRadius) # RPM
    finalRPM = finalRPM * 0.10472 # rad/s
    A = - (MOMENTINERTIA + pow(gearRatio, 2) * pow(tireRadius, 2) * CARMASS)
    B = 1
    C = 1
    D = 1
    return quad(lambda RPM: - (MOMENTINERTIA + pow(gearRatio, 2) * pow(tireRadius, 2) * CARMASS) / (gearRatio * tireRadius * (DRAGCOEFFICIENT * AIRDENSITY * AREA / 2 * pow(2 * math.pi * tireRadius * gearRatio * RPM, 2)+ 4 * RESISTIVECOEFFICIENT * (CARWEIGHT * math.cos(INCLINEANGLE) + LIFTCOEFFICIENT * AIRDENSITY * AREA / 2 * pow(2 * math.pi * tireRadius * gearRatio * RPM, 2)) + CARWEIGHT * math.sin(INCLINEANGLE)) + INTERNALFRICTION - MOTORTORQUE), initialRPM, finalRPM)[0]

def calc_zts(gearLB, gearUB):
    i = 0
    pointCount = 10000
    while i < pointCount:
        ztsRatio.append(gearLB + (gearUB - gearLB) / pointCount * i)
        ztsTime.append(quick_calc(0, 88, gearLB + (gearUB - gearLB) / pointCount * i))
        i += 1

def create_xlsx():
    df = pd.DataFrame({"Gear Ratio":ztsRatio,"ZTS Time":ztsTime})
    writer = pd.ExcelWriter('Zero_to_Sixty_Time.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name="Sheet1")
    writer.save()

def attempt_one(initialVelocity, finalVelocity): # -0.8699522189645782
    finalRPM = 60 * finalVelocity / (2 * math.pi * tireRadius) # RPM
    initialRPM = 60 * initialVelocity / (2 * math.pi * tireRadius) # RPM
    h = 2 * 3.1415926 * tireRadius * gearRatio # 29.321
    a = CARMASS * tireRadius * gearRatio # 86.957
    b = 0.5 * AIRDENSITY * AREA * h * h * (DRAGCOEFFICIENT + 4 * RESISTIVECOEFFICIENT * LIFTCOEFFICIENT) # 1.6767
    c = 4 * RESISTIVECOEFFICIENT * CARWEIGHT * math.cos(INCLINEANGLE) + CARWEIGHT * math.sin(INCLINEANGLE) # 36.000
    D = - (MOMENTINERTIA + gearRatio * tireRadius * a) # -405.9
    E = gearRatio * tireRadius * b # 7.8246
    F = E * c + INTERNALFRICTION - MOTORTORQUE # 197.87
    sqrtEF = pow(E * F, 1/2)
    return D * sqrtEF / (E * F) * math.atan(sqrtEF * finalRPM / F) # Correct integral

def attempt_two(initialVelocity, finalVelocity): # -7.913456655180938
    finalRPM = 60 * finalVelocity / (2 * math.pi * tireRadius) # RPM
    initialRPM = 60 * initialVelocity / (2 * math.pi * tireRadius) # RPM
    finalRPM = finalRPM * 0.10472  # rad/s
    R = gearRatio * tireRadius
    D = DRAGCOEFFICIENT * AIRDENSITY * AREA / 2
    l = 2 * math.pi * tireRadius * gearRatio
    C = CARWEIGHT * math.cos(INCLINEANGLE)
    L = LIFTCOEFFICIENT * AIRDENSITY * AREA / 2
    S = CARWEIGHT * math.sin(INCLINEANGLE)
    T = INTERNALFRICTION - MOTORTORQUE
    a = - (MOMENTINERTIA + pow(R, 2) * CARMASS)
    b = R * D * pow(l, 2) + 4 * RESISTIVECOEFFICIENT * R * L * pow(l, 2)
    c = 4 * RESISTIVECOEFFICIENT * C * R + R * S + T
    return a * math.atan(b * (finalRPM - initialRPM) / pow(b * c, 1/2)) / pow(b * c, 1/2)


calc_zts(3,7)
create_xlsx()
