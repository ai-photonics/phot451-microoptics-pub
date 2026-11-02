import numpy as np
import matplotlib.pyplot as plt

from optiland import optic

singlet = optic.Optic()

# define surfaces
singlet.surfaces.add(index=0, radius=np.inf, thickness=np.inf)
singlet.surfaces.add(
    index=1, radius=0.2, thickness=0.05, is_stop=True, material="N-SF11"
)
singlet.surfaces.add(index=2, radius=np.inf, thickness=0.25)
singlet.surfaces.add(index=3)

# define aperture
singlet.set_aperture(aperture_type="EPD", value=0.2)

# define fields
singlet.fields.set_type(field_type="angle")
singlet.fields.add(y=0)
singlet.fields.add(y=10)
singlet.fields.add(y=20)

# define wavelengths
singlet.wavelengths.add(value=0.5, is_primary=True)

# draw it
singlet.draw(num_rays=10)
plt.show()
