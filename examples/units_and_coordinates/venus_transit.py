"""
==============================================
Overplotting the position of the Venus transit
==============================================

How to accurately plot the position of Venus as it transitted in front
of the Sun as observed by SDO/AIA.
"""
import matplotlib.pyplot as plt

import astropy.units as u
from astropy.coordinates import SkyCoord
from astropy.coordinates import solar_system_ephemeris

from sunpy.net import Fido, attrs as a
import sunpy.map
from sunpy.coordinates import get_body_heliographic_stonyhurst

###############################################################################
# Let's download an image of the Venus transit.
result = Fido.search(a.Time('2012/06/06 04:07:25', '2012/06/06 04:07:35'),
                     a.Instrument('aia'),
                     a.Wavelength(1600*u.angstrom))
files = Fido.fetch(result)
aiamap = sunpy.map.Map(files[0])

###############################################################################
# For this example, we require high-precision ephemeris information. The built-in
# ephemeris provided by astropy is not accurate enough. This call requires ``jplephem``
# to be installed. This will also trigger a download of about ~10 MB.
solar_system_ephemeris.set('de432s')

###############################################################################
# Now we get the position of Venus and convert it into the SDO/AIA coordinates.
# The apparent position of Venus accounts for the time it takes for light to
# travel from Venus to SDO.
venus = get_body_heliographic_stonyhurst('venus', aiamap.date, observer=aiamap.observer_coordinate)
venus_hpc = venus.transform_to(aiamap.coordinate_frame)

###############################################################################
# Let's crop the image with Venus at its center.
fov = 100 * u.arcsec
top_right = SkyCoord(venus_hpc.Tx + fov, venus_hpc.Ty + fov, frame=aiamap.coordinate_frame)
bottom_left = SkyCoord(venus_hpc.Tx - fov, venus_hpc.Ty - fov, frame=aiamap.coordinate_frame)
smap = aiamap.submap(top_right, bottom_left)

###############################################################################
# Let's plot the results.
ax = plt.subplot(projection=smap)
smap.plot()
smap.draw_limb()
ax.grid(False)
ax.plot_coord(venus_hpc, 'x', color='deepskyblue', label='Venus')
plt.legend()
plt.show()
