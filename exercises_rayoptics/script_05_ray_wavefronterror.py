import numpy as np
import matplotlib.pyplot as plt
from optiland import optic

# --- Create the optical system
singlet = optic.Optic()

# define surfaces
singlet.surfaces.add(index=0, radius=np.inf, thickness=np.inf)
singlet.surfaces.add(index=1, radius=20, thickness=7, is_stop=True, material="N-SF11")
singlet.surfaces.add(index=2, radius=np.inf, thickness=20.94)
singlet.surfaces.add(index=3)

# define aperture
singlet.set_aperture(aperture_type="EPD", value=5)

# define fields
singlet.fields.set_type(field_type="angle")
singlet.fields.add(y=0)
singlet.fields.add(y=10)

# define wavelengths
singlet.wavelengths.add(value=0.5, is_primary=True)

# draw it
singlet.draw(num_rays=10)
# ---------------------------------------


# --- Analysis: Calculate the PSF
from optiland import wavefront
opd_fan = wavefront.OPDFan(singlet)
opd_fan.view()

# Show all plots
plt.show()
