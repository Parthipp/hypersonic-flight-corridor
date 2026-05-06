import numpy as np
from atmosphere import get_density
from aerothermal import get_dynamic_pressure, get_heatflux

Nose_Radius = 0.15
Q_max = 50000
Q_min = 10000
Heat_Flux_Max = 3000000

def define_corridor_at_velocity(velocity,
                                q_max=Q_max,
                                q_min=Q_min,
                                nose_radius=Nose_Radius):
    """At a given velocity, find the max and min altitude at which that defines the flyable corridor.
    
    Return:
    alt_min : minimum altitude (lower-boundary - dynamic pressure limit)
    alt_max : maximum altitude (upper-boundary - heating limit)
    """

    altitudes = np.linspace(10000, 80000, 500)

    alt_min = None
    alt_max = None
    
    for h in altitudes:
        q_dyn = get_dynamic_pressure(velocity, h)
        q_heat = get_heatflux(velocity, h, Nose_Radius)

        if q_dyn <= q_max and alt_min is None:
            alt_min = h
        
        if q_dyn >= q_min:
            alt_max = h
        
    return alt_min, alt_max

from atmosphere import get_density
from aerothermal import get_heatflux

test_velocity = 1820 

alt_min, alt_max =  define_corridor_at_velocity(test_velocity)

print(f"\nCorridor at V = {test_velocity} m/s (~Mach 6):")

if alt_min:
    print(f"  Lower boundary (structural limit) = {alt_min/1000:.1f} km")
else:
    print(f"  Lower boundary = Not found")

if alt_max:
    print(f"  Upper boundary (scramjet limit)   = {alt_max/1000:.1f} km")
else:
    print(f"  Upper boundary = Not found")

if alt_min and alt_max and alt_max > alt_min:
    print(f"  Corridor width = {(alt_max - alt_min)/1000:.1f} km")
else:
    print(f"  No valid corridor found")