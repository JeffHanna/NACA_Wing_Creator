# NACA Wing Creator

A Python library for generating NACA airfoil coordinates with support for 4-digit and 5-digit series. This tool calculates the precise geometric profiles used in aerospace engineering for wing cross-sections.

## Features

- ✈️ **NACA 4-Series**: Analytical calculations for symmetric and cambered airfoils
- ✈️ **NACA 5-Series**: Support for more complex airfoil shapes with reflex camber
- 📊 **Flexible Point Distribution**: Configurable number of points with optional cosine spacing for enhanced leading edge resolution
- 🎯 **Ready-to-Plot Output**: Returns complete airfoil outlines as NumPy arrays
- 🧪 **Well-Tested**: Comprehensive unit test coverage
- 📈 **Visualization Examples**: Includes plotting examples for common aircraft airfoils

## Installation

Clone the repository:

```bash
git clone https://github.com/JeffHanna/NACA_Wing_Creator.git
cd NACA_Wing_Creator
```

Install dependencies:

```bash
pip install numpy matplotlib
```

## Quick Start

### NACA 4-Series Airfoil

```python
from naca import NACA_4

# Create a NACA 2412 airfoil (2% camber, 40% location, 12% thickness)
airfoil = NACA_4("2412", num_points=200, half_cosine_spacing=True)
x, y = airfoil.points

# Plot
import matplotlib.pyplot as plt
plt.plot(x, y)
plt.axis('equal')
plt.grid(True)
plt.xlabel('x/c')
plt.ylabel('y/c')
plt.title('NACA 2412 Airfoil')
plt.show()
```

### NACA 5-Series Airfoil

```python
from naca import NACA_5

# Create a NACA 23016 airfoil (Cl=0.3, 15% camber location, 16% thickness)
airfoil = NACA_5("23016", num_points=200)
x, y = airfoil.points
```

## Usage

### Parameters

All NACA classes accept the following parameters:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `naca_number` | str | Required | NACA designation (e.g., "2412", "23016") |
| `num_points` | int | 200 | Number of points per surface (upper/lower) |
| `half_cosine_spacing` | bool | True | Use cosine spacing for better leading edge resolution |

### Understanding NACA Numbering

#### 4-Digit Series (e.g., NACA 2412)
- **First digit (2)**: Maximum camber as % of chord (2%)
- **Second digit (4)**: Location of max camber in tenths of chord (40% from leading edge)
- **Last two digits (12)**: Maximum thickness as % of chord (12%)

#### 5-Digit Series (e.g., NACA 23016)
- **First digit (2)**: Design lift coefficient × 2/3 (Cl = 0.3)
- **Second & third digits (30)**: Location of max camber in half-percent of chord (15%)
- **Fourth digit (1)**: Reflex camber indicator (0=simple, 1=reflex)
- **Last two digits (16)**: Maximum thickness as % of chord (16%)

## Examples

The repository includes [`example_plot.py`](example_plot.py) which demonstrates plotting airfoils used in famous aircraft:

- **Boeing B-17**: NACA 0018 (root), NACA 0010 (tip)
- **Lockheed P-38**: NACA 23016 (root), NACA 4412 (tip)
- **Cessna 172**: NACA 2412 (root and tip)

Run the examples:

```bash
python example_plot.py
```

### Comparing Multiple Airfoils

```python
from naca import NACA_4, NACA_5
import matplotlib.pyplot as plt

# Create different airfoils
symmetric = NACA_4("0012")
cambered_4 = NACA_4("2412")
cambered_5 = NACA_5("23012")

# Plot comparison
plt.figure(figsize=(12, 6))
plt.plot(*symmetric.points, label="NACA 0012 (Symmetric)")
plt.plot(*cambered_4.points, label="NACA 2412 (4-series)")
plt.plot(*cambered_5.points, label="NACA 23012 (5-series)")
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
from naca import NACA_4

airfoil = NACA_4("2412", num_points=100)
x, y = airfoil.points

# Save coordinates to file
np.savetxt('naca2412.csv', np.column_stack([x, y]), 
           delimiter=',', header='x,y', comments='')
```

## API Reference

### NACA_4

Generates NACA 4-digit series airfoil coordinates using analytical equations.

**Properties:**
- `points`: Returns `(x_array, y_array)` tuple with complete airfoil outline
- `naca_number`: The NACA designation being used
- `x_points`: X-axis points along the mean camber line

### NACA_5

Generates NACA 5-digit series airfoil coordinates using analytical equations with tabulated mean line data.

**Properties:**
- `points`: Returns `(x_array, y_array)` tuple with complete airfoil outline
- `naca_number`: The NACA designation being used
- `x_points`: X-axis points along the mean camber line

**Supported 5-digit configurations:** 210, 220, 221, 230, 231, 240, 241, 250, 251

## Testing

Run the test suite:

```bash
python -m unittest test_naca.py
```

The test suite includes:
- Point count validation
- Data structure verification
- Symmetric airfoil validation
- Coordinate range testing
- Leading/trailing edge position checks

## Technical Details

### Coordinate System

All coordinates are normalized by chord length (c), so x and y values range from 0 to 1 (or ±1 for y depending on airfoil shape).

### Point Distribution

The outline path goes: **trailing edge (upper) → leading edge → trailing edge (lower)**

With `half_cosine_spacing=True`, points are concentrated near the leading edge where curvature is greatest, providing better geometric fidelity.

### Calculations

The library uses the standard NACA equations as documented:
- [Wikipedia: NACA Airfoil](https://en.wikipedia.org/wiki/NACA_airfoil)
- [Airfoil Tools: 4-Digit](http://airfoiltools.com/airfoil/naca4digit)
- [Airfoil Tools: 5-Digit](http://airfoiltools.com/airfoil/naca5digit)

## License

This project is open source. See the repository for license details.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## References

- NACA (National Advisory Committee for Aeronautics) - the predecessor to NASA
- Standard airfoil equations and coefficients from NACA technical reports
- Validated against published airfoil coordinates

## Author

Jeff Hanna ([@JeffHanna](https://github.com/JeffHanna))

---

*For detailed usage instructions, see [USAGE.md](USAGE.md)*
