# NACA Wing Creator - Usage Guide

## Overview

This module provides classes for generating NACA airfoil coordinates:
- **NACA_4**: 4-digit series (calculated analytically)
- **NACA_5**: 5-digit series (calculated analytically)

## Installation

No special installation required beyond standard Python packages:
```bash
pip install numpy matplotlib
```

## Quick Start

### NACA 4-Series
```python
from naca import NACA_4

# Create a NACA 2412 airfoil with 200 points
airfoil = NACA_4("2412", num_points=200, half_cosine_spacing=True)
x, y = airfoil.points

# Plot
import matplotlib.pyplot as plt
plt.plot(x, y)
plt.axis('equal')
plt.show()
```

### NACA 5-Series
```python
from naca import NACA_5

# Create a NACA 23016 airfoil
airfoil = NACA_5("23016", num_points=200)
x, y = airfoil.points
```


## Parameters

All classes accept these parameters:

- **naca_number** (str): The NACA designation (e.g., "2412", "23016", "64012")
- **num_points** (int, optional): Number of points per surface (default: 200)
- **half_cosine_spacing** (bool, optional): Use cosine spacing for better leading edge resolution (default: True)



## Examples

### Compare Multiple Airfoils
```python
from naca import NACA_4, NACA_5, NACA_6
import matplotlib.pyplot as plt

# Create airfoils
naca4 = NACA_4("0012", num_points=200)
naca5 = NACA_5("23012", num_points=200)

# Plot comparison
plt.figure(figsize=(12, 6))
plt.plot(*naca4.points, label="NACA 0012 (4-series)")
plt.plot(*naca5.points, label="NACA 23012 (5-series)")
plt.axis('equal')
plt.grid(True)
plt.legend()
plt.xlabel('x/c')
plt.ylabel('y/c')
plt.title('NACA Airfoil Comparison')
plt.show()
```

### Export to CSV
```python
import numpy as np

airfoil = NACA_4("2412", num_points=100)
x, y = airfoil.points

# Save to file
np.savetxt('naca2412.csv', np.column_stack([x, y]), 
           delimiter=',', header='x,y', comments='')
```

## Understanding NACA Numbering

### 4-Digit Series (e.g., NACA 2412)
- **2**: Maximum camber (2% of chord)
- **4**: Location of max camber (40% from leading edge)
- **12**: Maximum thickness (12% of chord)

### 5-Digit Series (e.g., NACA 23016)
- **2**: Design lift coefficient × 2/3 (Cl = 0.3)
- **30**: Location of max camber (15% from leading edge)
- **16**: Maximum thickness (16% of chord)


## Troubleshooting

### Import Errors
**Problem:** `ModuleNotFoundError: No module named 'numpy'`

**Solution:**
```bash
pip install numpy matplotlib
```

## References

- Wikipedia NACA Airfoil: https://en.wikipedia.org/wiki/NACA_airfoil
- UIUC Airfoil Coordinate Database: https://m-selig.ae.illinois.edu/ads/coord_database.html
- NASA Technical Reports: https://ntrs.nasa.gov/

## License

See repository LICENSE file for details.
