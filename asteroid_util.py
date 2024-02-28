from poliastro.bodies import Sun, Earth
from poliastro.frames import Planes
from poliastro.plotting import StaticOrbitPlotter
from poliastro.twobody import Orbit
from poliastro.ephem import Ephem
from astropy.time import Time
import matplotlib.pyplot as plt
from os import remove

earth_semimajor_axis = 1.0 # AU
earth_eccentricity = 0.0167


def plot_asteroid_orbit_from_id(asteroid_id, asteroid_name, date_time): 

    epoch = Time(date_time, scale='tdb')

    plotter = StaticOrbitPlotter(plane=Planes.EARTH_ECLIPTIC)
    earth_plots_traj, earth_plots_pos = plotter.plot_body_orbit(Earth, epoch, label='Earth')
    earth_plots_pos.set_markersize(10)

    asteroid = Orbit.from_sbdb(asteroid_id)
    asteroid = asteroid.propagate(epoch)

    asteroid_plots_traj, asteroid_plots_pos = plotter.plot(asteroid, label=asteroid_name, color='red')

    plt.savefig(f'tmp/{asteroid_id}.png', bbox_inches='tight')


def get_from_asteroid_id(asteroid_id): 
    return(f'tmp/{asteroid_id}.png')

def delete_asteroid_plot(asteroid_id): 
    remove(f'tmp/{asteroid_id}.png')

plot_asteroid_orbit_from_id(3422140, '2008 OS7', "2024-02-02 14:41")