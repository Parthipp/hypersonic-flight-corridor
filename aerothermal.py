import numpy as np
from atmosphere import get_density

K = 1.7415e-4

def get_heatflux(velocity, altitude, nose_radius):
    """Calculate stagnation point heat flux using Sutton-Graves equation
    
    Parameters: 
    Velocity : Vehicle Velocity
    Altitude : altitude(m)
    nose radius: nose radius of vehicle(m)
    
    Returns:
    heat flux : stagnation heat flux (W/m^2)
    """
    rho = get_density(altitude)

    heat_flux = K * np.sqrt(rho / nose_radius) * velocity**3
    return heat_flux

def get_dynamic_pressure(velocity, altitude):
    """Calculate dynamic pressure (Structural load on the vehicle)
    
    Parameters:
    velocity : velocity of the vehicle m/s
    altitude : altitude m
    
    returns:
    dynamic pressure : dynamic pressure Pa
    """
    rho = get_density(altitude)

    dyn_pressure = 0.5 * rho * velocity**2
    return dyn_pressure

velo = 1500
alt = 25000
nose_rad = 0.15

q_heat = get_heatflux(velo, alt, nose_rad)
q_dyn = get_dynamic_pressure(velo, alt)

print(f"\nhypersonic heating test: ")
print(f"  Heat Flux        = {q_heat/1000:.2f} kW/m²")
print(f"  Dynamic Pressure = {q_dyn/1000:.2f} kPa")
print(f"  Dynamic Pressure = {q_dyn:.2f} Pa")