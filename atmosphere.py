import numpy as np

#sea level constants
T0 = 288.15  #Temp at sea level
P0 = 101325  # Pressure at sea level
R = 287.05   # Gas constant for air

def get_temp(altitude):
    """Calculate temperature at given altitude"""  
    if altitude <= 11000:
        lapse_rate = -0.0065
        temp = T0 + lapse_rate * altitude
    elif altitude <= 20000:
        temp = 216.65
    elif altitude <= 32000:
        lapse_rate = 0.001
        temp = 216.65 + lapse_rate * (altitude - 20000)
    else:
        temp = 228.65
    return temp

def get_pressure(altitude):
    """Calculate pressure at given altitude"""
    g = 9.80665   
    
    if altitude <= 11000:
        T = T0 + (-0.0065 * altitude)
        pressure = P0 * (T / T0) ** (g / (R * 0.0065))
    
    elif altitude <= 20000:
        P_11km = 22632.1   
        T_11km = 216.65    
        pressure = P_11km * np.exp(-g * (altitude - 11000) / (R * T_11km))
    
    elif altitude <= 32000:
        P_20km = 5474.89   
        T_20km = 216.65    
        lapse_rate = 0.001
        T = T_20km + lapse_rate * (altitude - 20000)
        pressure = P_20km * (T / T_20km) ** (-g / (R * lapse_rate))
    
    else:
        P_32km = 868.019   
        T_32km = 228.65    
        lapse_rate = 0.0028
        T = T_32km + lapse_rate * (altitude - 32000)
        pressure = P_32km * (T / T_32km) ** (-g / (R * lapse_rate))
    
    return pressure

def get_density(altitude):
    """Calculate density at given altitude"""
    temp = get_temp(altitude)
    press = get_pressure(altitude)
    
    density = press / (R * temp)
    return density
