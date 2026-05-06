import numpy as np
import matplotlib.pyplot as plt
from corridor import define_corridor_at_velocity, Nose_Radius, Q_max, Q_min
from aerothermal import get_heatflux, get_dynamic_pressure

# Vehicle Definitions

Vehicles = [
    {
        'name' : 'X-51A Waverider',
        'nose_radius' : 0.15,
        'q_max' : 50000,
        'q_min' : 10000,
        'color' : 'blue',
        'data_point' : (1550, 21),
        'data_label' : 'X-51A (Mach 5.1, 21Km)'
    },
    {
        'name' : 'X-43A Hyper-X',
        'nose_radius' : 0.10,
        'q_max' : 95000,
        'q_min' : 15000,
        'color' : 'red',
        'data_point' : (2940, 33.5),
        'data_label' : 'X-43A (Mach 9.68, 33.5Km)'
    },
    {
        'name' : 'Generic Concept Vehicle',
        'nose_radius' : 0.30,
        'q_max' : 35000,
        'q_min' : 8000,
        'color' : 'green',
        'data_point' : None,
        'data_label' : None
    }
]

velocities = np.linspace(1515, 3030, 50)

results = []

for vehicle in Vehicles:
    print(f"\nCalculating corridor for {vehicle['name']}...")
    
    lower_bounds = []
    upper_bounds = []
    valid_velocities = []

    for v in velocities:
        alt_min, alt_max = define_corridor_at_velocity(
            v, 
            q_max = vehicle['q_max'],
            q_min = vehicle['q_min'],
            nose_radius = vehicle['nose_radius']
        )

        if alt_min is not None and alt_max is not None:
            if alt_max > alt_min:
                lower_bounds.append(alt_min/1000)
                upper_bounds.append(alt_max/1000)
                valid_velocities.append(v)

    results.append({
        'vehicle' : vehicle,
        'velocities' : np.array(valid_velocities),
        'lower' : np.array(lower_bounds),
        'upper' : np.array(upper_bounds)
    })

    print(f" Found corridors at {len(valid_velocities)} velocity points")

print("\nAll corridors calculated")

fig, ax = plt.subplots(figsize=(13, 8))

for result in results:
    v       = result['velocities']
    lower   = result['lower']
    upper   = result['upper']
    vehicle = result['vehicle']
    color   = vehicle['color']
    name    = vehicle['name']
    
    # Shade the corridor
    ax.fill_between(v, lower, upper,
                    alpha=0.15,
                    color=color)
    
    # Plot boundary lines
    ax.plot(v, lower, color=color, linewidth=2,
            linestyle='--')
    ax.plot(v, upper, color=color, linewidth=2,
            label=name)
    
    # Plot real flight data points if available
    if vehicle['data_point'] is not None:
        vx, vy = vehicle['data_point']
        ax.scatter(vx, vy,
                   color=color, s=200,
                   zorder=5, marker='*')
        ax.annotate(vehicle['data_label'] + '\n(rocket boosted)',
                    xy=(vx, vy),
                    xytext=(vx + 80, vy + 3),
                    fontsize=9,
                    fontweight='bold',
                    arrowprops=dict(arrowstyle='->',
                                   color=color))


# FORMATTING

ax.set_xlabel('Velocity (m/s)', fontsize=13)
ax.set_ylabel('Altitude (km)', fontsize=13)
ax.set_title('Hypersonic Flight Corridor Comparison\nAir-Breathing Vehicles (Mach 5–10)',
             fontsize=14, fontweight='bold')

ax.legend(fontsize=10, loc='upper left',
          title='Vehicle (solid=upper, dashed=lower boundary)',
          title_fontsize=9)
ax.grid(True, alpha=0.3)
ax.set_ylim(0, 60)
ax.set_xlim(1400, 3100)

# Mach number labels on top axis
ax2 = ax.twiny()
ax2.set_xlim(ax.get_xlim())
mach_ticks  = [1515, 1818, 2121, 2424, 2727, 3030]
mach_labels = ['M5', 'M6', 'M7', 'M8', 'M9', 'M10']
ax2.set_xticks(mach_ticks)
ax2.set_xticklabels(mach_labels, fontsize=11)
ax2.set_xlabel('Mach Number', fontsize=13)

# Vehicle parameter summary box
param_text = (
    "Vehicle Parameters\n"
    "─────────────────────────────\n"
    f"X-51A  │ Rn=0.15m │ q: 10–50 kPa\n"
    f"X-43A  │ Rn=0.10m │ q: 15–95 kPa\n"
    f"Concept│ Rn=0.30m │ q:  8–35 kPa"
)
props = dict(boxstyle='round', facecolor='wheat', alpha=0.6)
ax.text(0.98, 0.05, param_text,
        transform=ax.transAxes,
        fontsize=9,
        verticalalignment='bottom',
        horizontalalignment='right',
        bbox=props,
        fontfamily='monospace')

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig('hypersonic_corridor_comparison.png', dpi=200, bbox_inches='tight')
plt.show()

print("\n✅ Plot saved as hypersonic_corridor_comparison.png")

