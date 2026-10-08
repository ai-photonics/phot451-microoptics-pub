import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from optiland import optic

scene = optic.Optic()

# Add surfaces: this will form the lenses
scene.surfaces.add(index=0, thickness=np.inf)
scene.surfaces.add(index=1, thickness=7.0, radius=20.0, is_stop=True, material="N-SF11")
scene.surfaces.add(index=2, thickness=23.0)
scene.surfaces.add(index=3)

# Aperture
scene.set_aperture(aperture_type="EPD", value=20.0)

# Definition EM-field
scene.fields.set_type(field_type="angle")
scene.fields.add(y=10)
#
scene.wavelengths.add(value=0.65, is_primary=True)

scene.draw(num_rays=10)
plt.show()
