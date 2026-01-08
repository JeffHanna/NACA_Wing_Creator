"""
Example of how to plot NACA airfoil profiles.

Both NACA_4 and NACA_5 now return points ready to plot:
- points[0]: x coordinates for the complete airfoil outline
- points[1]: y coordinates for the complete airfoil outline

The outline goes: trailing edge (upper) -> leading edge -> trailing edge (lower)
"""
import matplotlib.pyplot as plt
from naca import NACA_4, NACA_5


def _plot_airfoils(root: NACA_4 | NACA_5, tip: NACA_4 | NACA_5, root_label: str, tip_label: str):
    """Helper function to plot root and tip airfoils side by side."""
    root_x, root_y = root.points
    tip_x, tip_y = tip.points
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    ax1.plot(root_x, root_y, 'b-', linewidth=2)
    ax1.set_title(f'{root_label} Airfoil')
    ax1.set_xlabel('x/c')
    ax1.set_ylabel('y/c')
    ax1.set_aspect('equal')
    ax1.grid(True, alpha=0.3)
    ax2.plot(tip_x, tip_y, 'r-', linewidth=2)
    ax2.set_title(f'{tip_label} Airfoil')
    ax2.set_xlabel('x/c')
    ax2.set_ylabel('y/c')
    ax2.set_aspect('equal')
    ax2.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

# B-17 Airfoils
b_17_root = NACA_4('0018')  # B-17 Root
b_17_tip = NACA_4('0010')  # B-17 Tip
_plot_airfoils(b_17_root, b_17_tip, 'B-17 Root', 'B-17 Tip')

# P-38 Airfoils
p_38_root = NACA_5('23016')  # P-38 Root
p_38_tip = NACA_4('4412')  # P-38 Tip
_plot_airfoils(p_38_root, p_38_tip, 'P-38 Root', 'P-38 Tip')

# C-172 Airfoils
c_172_root = NACA_4('2412')  # C-172 Root
c_172_tip = NACA_4('2412')  # C-172 Tip
_plot_airfoils(c_172_root, c_172_tip, 'C-172 Root', 'C-172 Tip')
