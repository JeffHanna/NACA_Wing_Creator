"""
Example of how to plot NACA airfoil profiles.

Both NACA_4 and NACA_5 now return points ready to plot:
- points[0]: x coordinates for the complete airfoil outline
- points[1]: y coordinates for the complete airfoil outline

The outline goes: trailing edge (upper) -> leading edge -> trailing edge (lower)
"""
import matplotlib.pyplot as plt
from naca import NACA_4, NACA_5

# Create airfoils
naca4 = NACA_4('0018')
naca5 = NACA_5('23112')

# Get points - both return (x_outline, y_outline) ready to plot!
x_4, y_4 = naca4.points
x_5, y_5 = naca5.points

# Plot
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

ax1.plot(x_4, y_4, 'b-', linewidth=2)
ax1.set_title('NACA 0018')
ax1.set_xlabel('x/c')
ax1.set_ylabel('y/c')
ax1.set_aspect('equal')
ax1.grid(True, alpha=0.3)

ax2.plot(x_5, y_5, 'r-', linewidth=2)
ax2.set_title('NACA 23112')
ax2.set_xlabel('x/c')
ax2.set_ylabel('y/c')
ax2.set_aspect('equal')
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
