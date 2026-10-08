# -------------------------------------------------------
# A first example script: using the "optiland" module
#  - Required to install the optiland package, see below links:
#       https://github.com/optiland/optiland
#       https://optiland.readthedocs.io/en/latest/
#       https://www.optiland.org/
# -------------------------------------------------------
import numpy as np

import matplotlib.pyplot as plt
from optiland import optic
from optiland.analysis import RayFan

# Create an empty optical system
lens = optic.Optic()

# Add surfaces: These will form the lens(es), object(source) plane, screen, etc.
lens.surfaces.add(index=0, thickness=np.inf)
lens.surfaces.add(index=1, thickness=7, radius=20.0, is_stop=True, material="N-SF11")
lens.surfaces.add(index=2, thickness=23.0)
lens.surfaces.add(index=3)

# add aperture to current lens
lens.set_aperture(aperture_type="EPD", value=20)

# add field: incoming rays of light
lens.fields.set_type(field_type="angle")
lens.fields.add(y=0)
lens.fields.add(y=10)
lens.fields.add(y=20)

# Choose the wavelengths used
lens.wavelengths.add(value=0.55, is_primary=True)

# Visualize the setup and rays
lens.draw(num_rays=10)

# Example analysis: Calculate and visualize Ray-fan plots
ray_fan = RayFan(lens, fields=[(0, 1)])
ray_fan = RayFan(lens)
ray_fan.view()

# Show all visualizations/plots
plt.show()
