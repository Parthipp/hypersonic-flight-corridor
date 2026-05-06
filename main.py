"""
Hypersonic Flight Corridor Mapper
===================================
Main entry point — runs the full pipeline:
1. Validates atmosphere model against standard tables
2. Runs aerothermal checks
3. Generates multi-vehicle corridor comparison plot
"""

from atmosphere import get_temperature, get_pressure, get_density
from aerothermal import get_heat_flux, get_dynamic_pressure

# QUICK ATMOSPHERE VALIDATION

print("=" * 50)
print("Hypersonic Flight Corridor Mapper")
print("=" * 50)

print("\n[1] Validating atmosphere model...")

checks = [
    (0,     288.15, 101325,  1.225),
    (10000, 223.15, 26436,   0.4127),
    (20000, 216.65, 5474.89, 0.08803),
    (25000, 221.65, 2511.02, 0.039466),
]

all_passed = True
for h, T_ref, P_ref, rho_ref in checks:
    T   = get_temperature(h)
    P   = get_pressure(h)
    rho = get_density(h)
    
    T_ok   = abs(T   - T_ref)   < 1.0
    P_ok   = abs(P   - P_ref)   < 50.0
    rho_ok = abs(rho - rho_ref) < 0.001
    
    status = "✓" if (T_ok and P_ok and rho_ok) else "✗"
    if not (T_ok and P_ok and rho_ok):
        all_passed = False
    
    print(f"  {status} At {h/1000:.0f} km: "
          f"T={T:.2f}K  P={P:.2f}Pa  rho={rho:.5f}kg/m³")

if all_passed:
    print("\n  ✓ Atmosphere model validated successfully!")
else:
    print("\n  ✗ Atmosphere model has errors — check atmosphere.py")

# QUICK AEROTHERMAL CHECK

print("\n[2] Running aerothermal check at Mach 6, 25 km...")

v        = 1820    # m/s (~Mach 6)
h        = 25000   # 25 km
Rn       = 0.15    # nose radius (m)

q_heat = get_heat_flux(v, h, Rn)
q_dyn  = get_dynamic_pressure(v, h)

print(f"  Heat flux       = {q_heat/1000:.2f} kW/m²")
print(f"  Dynamic pressure = {q_dyn/1000:.2f} kPa")

# GENERATE CORRIDOR PLOT

print("\n[3] Generating flight corridor comparison plot...")
print("    (This will take 15-20 seconds)\n")

import visualizer

print("\n✅ Done! Plot saved as hypersonic_corridor_comparison.png")