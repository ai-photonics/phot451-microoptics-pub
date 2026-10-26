import importlib.util
import numpy as np
import csv
from pathlib import Path
import h5py
from scipy import io
import matplotlib.pyplot as plt

# ============================================================
# Parameters
# ============================================================

# --- Output ---
project_root: str = "script_02_output"
run_name: str = "run_1"

# --- Session ---
# Adapt the path to the Lumerical API (lumapi.py) according to your installation
lumapi_path = Path("C:/Program Files/Lumerical/v261/api/python/lumapi.py")
# lumapi_path = Path("/opt/lumerical/v261/api/python/lumapi.py")
hide: bool = False
close: bool = False
run: bool = True
output_format: str = "hdf5"

# --- Constants ---
nm: float = 1.0e-9

# --- Scene ---
x_span = 2000 * nm
y_span = 2000 * nm
z_min = -8000 * nm
z_max = 4000 * nm
lens_curvature_radius = 3000 * nm
lens_thickness = 500 * nm
lens_radius = np.sqrt((2 * lens_curvature_radius - lens_thickness) * lens_thickness)
lens_x = 0 * nm
lens_y = 0 * nm
nfreq = 201

# ============================================================
# Initialization
# ============================================================

# Initiate FDTD
spec = importlib.util.spec_from_file_location("lumapi", str(lumapi_path))
lumapi = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lumapi)
print(f"[INFO] lumapi loaded from: {lumapi_path}")

# generate output folder
out_dir = Path(project_root) / run_name
out_dir.mkdir(parents=True, exist_ok=True)

# ============================================================
# Perform the FDTD simulation and save results
# ============================================================
with lumapi.FDTD(hide=hide) as fdtd:

    # Save the Lumerical file
    save_path = None
    save_path = (out_dir / f"{run_name}.fsp").resolve().as_posix()
    fdtd.save(save_path)

    # ============================================================
    # Build the FDTD scene
    # ============================================================

    # Prepare empty scene
    fdtd.eval("switchtolayout; deleteall;")

    # FDTD region
    fdtd.addfdtd()
    fdtd.set("x", 0)
    fdtd.set("y", 0)
    fdtd.set("z", 0)
    fdtd.set("x span", x_span)
    fdtd.set("y span", y_span)
    fdtd.set("z min", z_min)
    fdtd.set("z max", z_max)
    fdtd.set("x min bc", "PML")
    fdtd.set("y min bc", "PML")
    fdtd.set("z min bc", "PML")
    fdtd.set("x max bc", "PML")
    fdtd.set("y max bc", "PML")
    fdtd.set("z max bc", "PML")

    # Add microlens
    # First add sphere
    fdtd.addsphere()
    fdtd.set("material", "<Object defined dielectric>")
    fdtd.set("index", 2)
    fdtd.set("x", lens_x)
    fdtd.set("y", lens_y)
    fdtd.set("z", lens_curvature_radius - lens_thickness)
    fdtd.set("radius", lens_curvature_radius)
    # Now etch away part of the sphere
    fdtd.addrect()
    fdtd.set("material", "etch")
    fdtd.set("x", lens_x)
    fdtd.set("y", lens_y)
    fdtd.set("x span", 2.01 * lens_curvature_radius)
    fdtd.set("y span", 2.01 * lens_curvature_radius)
    fdtd.set("z min", 0)
    fdtd.set("z max", 2 * lens_curvature_radius)

    # Add source of light
    fdtd.addplane()
    fdtd.set("x", 0)
    fdtd.set("y", 0)
    fdtd.set("x span", x_span)
    fdtd.set("y span", y_span)
    fdtd.set("z", 0.99 * z_max)
    fdtd.set("direction", "Backward")

    # Add the monitor
    fdtd.adddftmonitor()
    fdtd.set("name", "monitor")
    fdtd.set("monitor type", "2D Y-normal")
    fdtd.set("override global monitor settings", True)
    fdtd.set("frequency points", nfreq)
    fdtd.set("x", 0)
    fdtd.set("y", 0)
    fdtd.set("z", 0)
    fdtd.set("x span", x_span)
    fdtd.set("z min", z_min)
    fdtd.set("z max", z_max)

    if run:
        # ============================================================
        # Run simulation
        # ============================================================
        fdtd.run()

        # ============================================================
        # Extract results and save them
        # ============================================================
        # Extract data variables & save variables to file
        result_names = ["x", "y", "z", "Ex", "Ey", "Ez"]
        if output_format == "hdf5":
            with h5py.File("results.hdf5", "w") as f:
                for result_name in result_names:
                    tmp = fdtd.getdata("monitor", result_name)
                    f[result_name] = tmp

        # ============================================================
        # Analysis and Plots (this is just an example)
        # ============================================================

    # Keep Lumerical open after finishing?
    if not close:
        input("press enter")
