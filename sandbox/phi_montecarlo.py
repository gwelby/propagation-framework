import math
import random
import numpy as np
import scipy.stats as stats
import datetime

# Electron and up quark masses
electron_mass = 0.000510999  # GeV
up_quark_mass = 0.0023  # GeV

# Golden ratio
phi = (1 + math.sqrt(5)) / 2

# Target ratio
target_ratio = phi**3

# Number of simulations
num_simulations = 100000

# Initialize counter for successful simulations
success_count = 0

# Perform simulations
for _ in range(num_simulations):
    # Generate random mass pairs from log-normal distribution
    random_electron_mass = np.random.lognormal(mean=np.log(electron_mass), sigma=0.1)
    random_up_quark_mass = np.random.lognormal(mean=np.log(up_quark_mass), sigma=0.1)
    
    # Calculate ratio
    ratio = random_electron_mass / random_up_quark_mass
    
    # Check if ratio is close to target ratio
    if abs(ratio - target_ratio) < 0.01:
        success_count += 1

# Calculate p-value
p_value = success_count / num_simulations

# Print results
print(f"p-value: {p_value:.6f}")

# Append results to sandbox_results.md
with open("D:\\Fundamentals\\sandbox\\sandbox_results.md", "a") as f:
    f.write(f"### {datetime.date.today()}\n")
    f.write(f"* Phi monte carlo test:\n")
    f.write(f"  + p-value: {p_value:.6f}\n")
    f.write(f"  + Electron mass: {electron_mass} GeV, Up quark mass: {up_quark_mass} GeV\n")

# Print "SIGNIFICANT" or "NOISE"
if p_value < 0.05:
    print("SIGNIFICANT")
else:
    print("NOISE")
