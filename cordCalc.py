import math
import tkinter as tk
from tkinter import messagebox, ttk

# convert altitude and azimuth (degrees) to radians
# then compute cartesian x,y,z for distance rly
def altaz_to_cartesian(rly, alt, az):
    theta = math.radians(90 - alt)
    phi = math.radians(az)
    x = rly * math.sin(theta) * math.cos(phi)
    y = rly * math.sin(theta) * math.sin(phi)
    z = rly * math.cos(theta)
    return x, y, z, theta, phi

def calculate_coordinates():
    try:
        r = float(entry_r.get())
        az = float(entry_az.get())
        alt = float(entry_alt.get())

        # compute cartesian coords and angles
        x, y, z, theta, phi = altaz_to_cartesian(r, alt, az)

        # show a brief textual result to the user
        result_text.set(
            f"φ: {math.degrees(phi):.1f}°, θ: {math.degrees(theta):.1f}°\n"
            f"X:{round(x)} ly  Y:{round(y)} ly  Z:{round(z)} ly"
        )

        # add a row to the history table (distance, az, alt, phi, theta, x, y, z)
        results_table.insert("", "end", values=(
            r, az, alt, f"{math.degrees(phi):.1f}", f"{math.degrees(theta):.1f}",
            f"{round(x)}", f"{round(y)}", f"{round(z)}"
        ))

        # try to update the averages footer; ignore errors
        try:
            compute_averages()
        except Exception:
            pass
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numeric values.")

# create gui window
root = tk.Tk()
root.title("Alt-Az to Cartesian Converter")
root.geometry("600x400")

# create notebook (tabbed interface)
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

# tab 1: conversion - inputs and convert button
frame_conversion = ttk.Frame(notebook)
notebook.add(frame_conversion, text="Converter")

# input fields: distance (ly), azimuth (deg), altitude (deg)
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

# tab 2: results table (history of conversions)
frame_results = ttk.Frame(notebook)
notebook.add(frame_results, text="Results History")

columns = ("Distance", "Azimuth", "Altitude", "Phi", "Theta", "X", "Y", "Z")
results_table = ttk.Treeview(frame_results, columns=columns, show="headings")

# set column headings and sizes
for col in columns:
    results_table.heading(col, text=col)
    results_table.column(col, width=80)

results_table.pack(expand=True, fill="both")

# averages footer frame: shows mean for each column
avg_frame = ttk.Frame(frame_results)
avg_frame.pack(side="bottom", fill="x", padx=5, pady=5)

# stringvars to hold average values (displayed in footer)
avg_vars = {col: tk.StringVar(value="—") for col in columns}

def compute_averages():
    # compute simple mean for each column from the table rows
    entries = results_table.get_children()
    if not entries:
        for c in columns:
            avg_vars[c].set("—")
        return
    sums = [0.0] * len(columns)
    for entry in entries:
        vals = results_table.item(entry, 'values') or ()
        for i, v in enumerate(vals):
            try:
                sums[i] += float(v)
            except Exception: # non-numeric table cells are ignored in sums
                pass
    n = len(entries)
    for i, c in enumerate(columns):
        avg = sums[i] / n

        avg_vars[c].set(f"{avg:.2f}" if c in ("Distance", "X", "Y", "Z") else f"{avg:.1f}")

def refresh_averages():
    compute_averages()

# footer labels
ttk.Label(avg_frame, text="Averages:").grid(row=0, column=0, padx=(0,8))
for i, col in enumerate(columns):
    ttk.Label(avg_frame, text=col+":").grid(row=0, column=1 + i*2, sticky="w")
    ttk.Label(avg_frame, textvariable=avg_vars[col], width=10).grid(row=0, column=2 + i*2, sticky="w")

# refresh button for the footer (manual update if it breaks for whatever reason)
ttk.Button(avg_frame, text="Refresh Averages", command=refresh_averages).grid(row=0, column=1 + len(columns)*2, padx=8)

compute_averages()

root.mainloop()
