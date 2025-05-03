import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk


#Variables
SECONDS_IN_YEAR = 365 * 24 * 3600
E_SN = 1.79e46  #energy per cubic lightyear in the interstellar medium 0.1 * 1.989 * 10^30kg *(300 000 000 m/s)^2
E_GN = 1.27e40  #energy per cubic lightyear in the intergalactic medium

def total_energy(D, scale, growth_rate):
    D = np.atleast_1d(D)
    
    #Energy in sphere under 500 light years
    sphere_energy = (4/3) * np.pi * (D/scale)**3 * E_SN
    
    # Initialize fraction_of_cap to 0 (no cap initially)
    fraction_of_cap = np.zeros_like(D)
    
    # Mask for spheres where D/scale > 500
    mask = (D/scale) > 500
    D_scaled = D[mask] / scale

    # radius of the sphere
    r = D_scaled 
    
    # Calculate spherical cap height (top and bottom)
    h = r - 500  # height of the spherical cap
    
    # Volume of spherical caps (i.e., truncated spheres)
    cap_volume = (np.pi * h**2 / 3) * (3 * r - h)
    
    ##Fraction of the energy removed
    fraction_of_cap[mask] = 2 * cap_volume *(E_SN-E_GN)/ ((4/3) * np.pi * r**3 * E_SN)  
    fraction_of_cap = np.clip(fraction_of_cap, 0, 1)
    
    # Apply cap loss (energy is reduced based on the truncated fraction)
    sphere_energy[mask] = sphere_energy[mask] * (1 - fraction_of_cap[mask])
    
    # Energy use at given growth
    growth_energy = (growth_rate**D) * 1e17 * SECONDS_IN_YEAR
    
    # Net energy calculation
    result = sphere_energy - growth_energy
    
    return result[0] if result.size == 1 else result

#Expansion rates
def energy_at_speed_0_1c_growth_1_percent(D):
    return total_energy(D, scale=10, growth_rate=1.01)

def energy_at_speed_0_5c_growth_1_percent(D):
    return total_energy(D, scale=5, growth_rate=1.01)

def energy_at_speed_1c_growth_1_percent(D):
    return total_energy(D, scale=1, growth_rate=1.01)

def energy_at_speed_0_1c_growth_2_percent(D):
    return total_energy(D, scale=10, growth_rate=1.02)

def energy_at_speed_0_5c_growth_2_percent(D):
    return total_energy(D, scale=5, growth_rate=1.02)

def energy_at_speed_1c_growth_2_percent(D):
    return total_energy(D, scale=1, growth_rate=1.02)

def energy_at_speed_0_1c_growth_3_percent(D):
    return total_energy(D, scale=10, growth_rate=1.03)

def energy_at_speed_0_5c_growth_3_percent(D):
    return total_energy(D, scale=5, growth_rate=1.03)

def energy_at_speed_1c_growth_3_percent(D):
    return total_energy(D, scale=1, growth_rate=1.03)


D_values = np.linspace(1, 10000, 10000)


# Plotting
plt.figure(figsize=(12, 7))

# Plot all the functions
plt.semilogy(D_values, energy_at_speed_0_1c_growth_1_percent(D_values), label=f'1% energy growth', color='blue')
plt.semilogy(D_values, energy_at_speed_0_5c_growth_1_percent(D_values), label=None, color='blue')
plt.semilogy(D_values, energy_at_speed_1c_growth_1_percent(D_values), label=None, color='blue')
plt.semilogy(D_values, energy_at_speed_0_1c_growth_2_percent(D_values), label=f'2% energy growth', color='orange')
plt.semilogy(D_values, energy_at_speed_0_5c_growth_2_percent(D_values), label=None, color='orange')
plt.semilogy(D_values, energy_at_speed_1c_growth_2_percent(D_values), label=None, color='orange')
plt.semilogy(D_values, energy_at_speed_0_1c_growth_3_percent(D_values), label=f'3% energy growth', color='yellow')
plt.semilogy(D_values, energy_at_speed_0_5c_growth_3_percent(D_values), label=None, color='yellow')
plt.semilogy(D_values, energy_at_speed_1c_growth_3_percent(D_values), label=None, color='yellow')

# Set axis labels and title
plt.xlabel("Time in years")
plt.ylabel("Usable Energy in joules (log scale)")
plt.title("Survival time of interstellar empires")
plt.xlim(0, 9000)
plt.ylim(1e45, 1e60)  # Adjust as needed
plt.yscale('log')  # Logarithmic scale for y-axis

from matplotlib.ticker import LogLocator

ax = plt.gca()
ax.set_yscale('log')

# Major ticks at 10^n
ax.yaxis.set_major_locator(LogLocator(base=10.0, numticks=15))

# Minor ticks at 2–9 * 10^n
ax.yaxis.set_minor_locator(LogLocator(base=10.0, subs=np.arange(2, 10), numticks=100))

# Enable gridlines
ax.grid(True, which='major', linestyle='--', linewidth=0.6)
ax.grid(True, which='minor', linestyle=':', linewidth=0.4, color='0.8')



#Legend placement
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))  # Moves legend outside the plot


# Labeling a specific point on the line (e.g., at D = 50)
y_01c_1p_value_at_50 = energy_at_speed_0_1c_growth_1_percent(5200) #E45 5200 #5000 E35 #1200 E1
plt.text(5000, y_01c_1p_value_at_50, '0.1c', fontsize=12, color='blue', verticalalignment='bottom')
y_05c_1p_value_at_50 = energy_at_speed_0_5c_growth_1_percent(5000) #E45 #5000 E35 #3800 E1
plt.text(5000, y_05c_1p_value_at_50, '0.5c', fontsize=12, color='blue', verticalalignment='bottom')
y_1c_1p_value_at_50 = energy_at_speed_1c_growth_1_percent(2800) #E45 2800 #3000 E35 #4200 E1
plt.text(5000, y_1c_1p_value_at_50, '1c', fontsize=12, color='blue', verticalalignment='bottom') 

y_01c_2p_value_at_50 = energy_at_speed_0_1c_growth_2_percent(3200) #E45 #3200 E35 #800 E1
plt.text(3000, y_01c_2p_value_at_50, '0.1c', fontsize=12, color="#FF8C00", verticalalignment='bottom')
y_05c_2p_value_at_50 = energy_at_speed_0_5c_growth_2_percent(3500) #E45 #3500 E35 #2800 E1
plt.text(3000, y_05c_2p_value_at_50, '0.5c', fontsize=12, color="#FF8C00", verticalalignment='bottom')
y_1c_2p_value_at_50 = energy_at_speed_1c_growth_2_percent(2200) #E45 #2200 E35 #2900 E1
plt.text(3000, y_1c_2p_value_at_50, '1c', fontsize=12, color="#FF8C00", verticalalignment='bottom')

y_01c_3p_value_at_50 = energy_at_speed_0_1c_growth_3_percent(1500) #E45 1500 #1400 E35 #300 E1
plt.text(1200, y_01c_3p_value_at_50, '0.1c', fontsize=12, color='#DBC205', verticalalignment='bottom')
y_05c_3p_value_at_50 = energy_at_speed_0_5c_growth_3_percent(1600) #E45 1600 #1400 E35 #1400 E1
plt.text(1200, y_05c_3p_value_at_50, '0.5c', fontsize=12, color='#DBC205', verticalalignment='bottom')
y_1c_3p_value_at_50 = energy_at_speed_1c_growth_3_percent(1200) #E45 1200 #1400 E35 #1200 E1
plt.text(1200, y_1c_3p_value_at_50, '1c', fontsize=12, color='#DBC205', verticalalignment='bottom')

# Adjust layout to avoid clipping
plt.tight_layout()

# Show the plot
plt.show()
