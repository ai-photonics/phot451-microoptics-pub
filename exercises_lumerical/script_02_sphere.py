import importlib.util
import numpy as np
import csv
from pathlib import Path


# ============================================================
# 1) Lumerical API loader
# ============================================================
def load_lumapi(verbose=True):
    lumapi_path = Path(
        "C:/Users/micha/OneDrive/Documents/LUMERICAL_2025R1.03_WINX64/Lumerical_Suite/custom_install_utility/2025R1/api/python/lumapi.py"
    )
    spec = importlib.util.spec_from_file_location("lumapi", str(lumapi_path))
    lumapi = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(lumapi)
    if verbose:
        print(f"[INFO] lumapi loaded from: {lumapi_path}")
    return lumapi


# ============================================================
# Parameters
# ============================================================

# --- Output ---
project_root: str = "script_01_output"
run_name: str = "run_1"

# --- Session ---
version_major: int = 25
hide: bool = False
save_fsp: bool = True
verbose: bool = True
close: bool = False
run: bool = False

# --- Constants ---
nm: float = 1.0e-9

# --- Scene ---
x_span = 2000 * nm
y_span = 4000 * nm
z_span = 2000 * nm
nfreq = 51


# ============================================================
# Initialization
# ============================================================

# Initiate FDTD and generate output folder
lumapi = load_lumapi(verbose=verbose)
out_dir = Path(project_root) / run_name
out_dir.mkdir(parents=True, exist_ok=True)

# ============================================================
# Perform the FDTD simulation and save results
# ============================================================
with lumapi.FDTD(hide=hide) as fdtd:

    save_path = None
    if save_fsp:
        save_path = (out_dir / f"{run_name}.fsp").resolve().as_posix()
        fdtd.save(save_path)

    # ============================================================
    # Build the FDTD scene
    # ============================================================
    # Prepare empty scene
    fdtd.eval("switchtolayout; deleteall;")
    # FDTD region
    fdtd.addfdtd()
    for k, v in {
        "dimension": "3D",
        "x": 0,
        "x span": x_span,
        "z": 0,
        "z span": z_span,
        "y": 0,
        "y span": y_span,
        "x min bc": "PML",
        "x max bc": "PML",
        "z min bc": "PML",
        "z max bc": "PML",
        "y min bc": "PML",
        "y max bc": "PML",
        "mesh accuracy": 4,
    }.items():
        fdtd.set(k, v)

    # Add a spherical object
    fdtd.addsphere()
    fdtd.set("name", "nanoparticle")
    fdtd.set("x", 0)
    fdtd.set("y", 0)
    fdtd.set("z", 0)
    fdtd.set("radius", 400 * nm)

    # Gaussian beam
    fdtd.addgaussian()
    fdtd.set("name", "Field monitor")
    fdtd.set("injection axis", "z")
    fdtd.set("direction", "backward")
    fdtd.set("x", 0)
    fdtd.set("x span", x_span)
    fdtd.set("y", 0)
    fdtd.set("y span", y_span)
    fdtd.set("z", 1000 * nm)
    fdtd.set("use scalar approximation", 1)
    fdtd.set("waist radius w0", 200 * nm)
    fdtd.set("distance from waist", 0 * nm)

    fdtd.adddftmonitor()
    # We could use fdtd.set(parameter, value):
    # fdtd.set("name", "Field monitor")
    # But we use dictionnaries to increase the readability
    for k, v in {
        "name": "Field monitor",
        "monitor type": "2d y-normal",
        "override global monitor settings": True,
        "frequency points": nfreq,
        "x": 0,
        "x span": x_span,
        "z": 0,
        "z span": z_span,
        "y": 0,
    }.items():
        fdtd.set(k, v)

    # ============================================================
    # Run simulation
    # ============================================================
    if run:
        fdtd.run()

    # Keep Lumerical open after finishing?
    if not close:
        input("press enter")
