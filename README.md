# SphericalConverter

A quick little Python GUI tool for converting celestial spherical coordinates (distance, azimuth, altitude) into Cartesian (x, y, z) coordinates.

## Features

- **Real-time Conversion**: Convert altitude/azimuth + distance into Cartesian x, y, z coordinates
- **Conversion History**: Track all conversions in a tabular format
- **Automatic Averaging**: Displays running averages for all columns (distance, angles, cartesian coordinates)
- **Tabbed Interface**: Easy navigation between the converter and results history
- **Input Validation**: Error handling for invalid numeric inputs
- **Manual Refresh**: Manually refresh averages if needed

## How It Works

The tool uses spherical coordinate transformation to convert:
- **Distance (r)**: Distance in light-years
- **Azimuth (φ)**: Horizontal angle in degrees (0–360°, measured from north)
- **Altitude (θ)**: Vertical angle in degrees (−90° to +90°, where 0° is horizon, 90° is zenith)

Into Cartesian coordinates:
- **X, Y, Z**: Position in light-years using standard spherical-to-Cartesian math

## Requirements

- Python 3.6+
- tkinter (usually included with Python)

## Installation

1. Clone or download this repository:
```bash
git clone https://github.com/yourusername/SphericalConverter.git
```

## Usage

Run the GUI:
```bash
python celestialSphericalToCartesian.py
```

### Converter Tab
1. Enter a **Distance** (in light-years)
2. Enter an **Azimuth** (0–360 degrees)
3. Enter an **Altitude** (−90 to +90 degrees)
4. Click **Convert**
5. View the result (Cartesian coordinates + spherical angles)

### Results History Tab
- View all conversions in a table
- See **Averages** footer showing per-column means
- Click **Refresh Averages** to manually recalculate if needed

## Example

**Input:**
- Distance: 100 ly
- Azimuth: 45°
- Altitude: 30°

**Output:**
- φ: 45.0°, θ: 60.0°
- X: 61 ly, Y: 61 ly, Z: 50 ly

## Technical Details

The conversion uses:
```
θ = 90° − altitude
φ = azimuth

x = r × sin(θ) × cos(φ)
y = r × sin(θ) × sin(φ)
z = r × cos(θ)
```

## Author

Brandon Erquicia

## Contributing

Contributions welcome! Feel free to open an issue or submit a pull request.