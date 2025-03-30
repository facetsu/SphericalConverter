import math
import tkinter as tk
from tkinter import messagebox, ttk

def altaz_to_cartesian(r_ly, alt_degrees, az_degrees):
    """
    Converts altitude-azimuth-distance (Alt, Az, r) to Cartesian coordinates (X, Y, Z).
    
    Parameters:
        r_ly (float): Distance in light-years.
        alt_degrees (float): Altitude in degrees (-90 to +90, where 0 is horizon, 90 is zenith).
        az_degrees (float): Azimuth in degrees (0 to 360, measured from north).
        
    Returns:
        tuple: (X, Y, Z, theta, phi) Cartesian coordinates and angles in light-years and radians.
    """
    theta = math.radians(90 - alt_degrees)  # Zenith angle
    phi = math.radians(az_degrees)          # Azimuth
    
    X = r_ly * math.sin(theta) * math.cos(phi)
    Y = r_ly * math.sin(theta) * math.sin(phi)
    Z = r_ly * math.cos(theta)
    
    return (X, Y, Z, theta, phi)

def calculate_coordinates():
    try:
        r = float(entry_r.get())
        az = float(entry_az.get())
        alt = float(entry_alt.get())
        
        X, Y, Z, theta, phi = altaz_to_cartesian(r, alt, az)
        
        result_text.set(f"Spherical Angles:\n"
                        f"  φ (Phi): {math.degrees(phi):.1f}°\n"
                        f"  θ (Theta): {math.degrees(theta):.1f}°\n\n"
                        f"Cartesian Coordinates (light-years):\n"
                        f"  X: {round(X)} ly\n"
                        f"  Y: {round(Y)} ly\n"
                        f"  Z: {round(Z)} ly")
        
        # Add to history table
        results_table.insert("", "end", values=(
            r, az, alt, f"{math.degrees(phi):.1f}", f"{math.degrees(theta):.1f}",
            f"{round(X)}", f"{round(Y)}", f"{round(Z)}"
        ))
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numeric values.")

# Create GUI window
root = tk.Tk()
root.title("Alt-Az to Cartesian Converter")
root.geometry("600x400")

# Create notebook (tabbed interface)
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

# Tab 1: Conversion
frame_conversion = ttk.Frame(notebook)
notebook.add(frame_conversion, text="Converter")

# Input fields
ttk.Label(frame_conversion, text="Distance (light-years):").pack()
entry_r = ttk.Entry(frame_conversion)
entry_r.pack()

ttk.Label(frame_conversion, text="Azimuth (degrees):").pack()
entry_az = ttk.Entry(frame_conversion)
entry_az.pack()

ttk.Label(frame_conversion, text="Altitude (degrees):").pack()
entry_alt = ttk.Entry(frame_conversion)
entry_alt.pack()

ttk.Button(frame_conversion, text="Convert", command=calculate_coordinates).pack()

result_text = tk.StringVar()
ttk.Label(frame_conversion, textvariable=result_text, justify="left").pack()

# Tab 2: Results Table
frame_results = ttk.Frame(notebook)
notebook.add(frame_results, text="Results History")

columns = ("Distance", "Azimuth", "Altitude", "Phi", "Theta", "X", "Y", "Z")
results_table = ttk.Treeview(frame_results, columns=columns, show="headings")

# Set column headings
for col in columns:
    results_table.heading(col, text=col)
    results_table.column(col, width=80)

results_table.pack(expand=True, fill="both")

root.mainloop()
