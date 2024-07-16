from matplotlib import pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.animation import FuncAnimation
import numpy as np
import math


def plot_mass_loss(container, time):
    x = np.linspace(0, time, len(container))
    y = [container[k] for k in range(len(container))]

    plt.plot(x, y, 'blue')
    plt.xlabel('Time')
    plt.ylabel('Mass loss')
    plt.show()


def plot_moss_loss_comparison(container_i, container_ii, time):
    x_i = np.linspace(0, time, len(container_i))
    y_i = [container_i[k] for k in range(len(container_i))]

    x_ii = np.linspace(0, time, len(container_ii))
    y_ii = [container_ii[k] for k in range(len(container_ii))]

    plt.plot(x_i, y_i, linewidth=3, color='blue')
    plt.plot(x_ii, y_ii, linewidth=1, color='red')

    plt.xlabel('time')
    plt.ylabel('mass loss')
    plt.show()




def plot_mass(mass_container, time):
    x = np.linspace(0, time, len(mass_container))
    y = [mass_container[k] for k in range(len(mass_container))]
    plt.plot(x, y, 'blue')
    plt.xlabel('Time')
    plt.ylabel('Total mass')
    plt.show()


def plot_central_density(central_container, time):
    x = np.linspace(0, time, len(central_container))
    y = [central_container[k] for k in range(len(central_container))]
    plt.plot(x, y, 'black')
    plt.xlabel('Time')
    plt.ylabel('Central Density')
    plt.show()


def plot_all_densities(container, radius, angle, freq):
    x = np.linspace(0, radius, len(container[0][0]))
    for k in range(len(container)):
        if k % freq == 0:
            radial_densities = np.zeros([len(container[0][0])])
            for i in range(len(container[0][0])):
                radial_densities[i] = container[k][i][angle]
            y = radial_densities

            plt.plot(x, y, 'blue')

    plt.xlabel('Radius')
    plt.ylabel('Density')
    plt.show()


# Additional feature : within the plot, specify which angle is being observed within the domain
def plot_final_density(container, radius, angle):
    final_state = container[len(container) - 1]
    radial_densities = np.zeros([len(container[0][0])])

    for i in range(len(final_state)):
        radial_densities[i] = final_state[i][angle]

    x = np.linspace(0, radius, len(container[0][0]))
    # y = [radial_densities[m] for m in range(len(radial_densities))]
    y = radial_densities

    plt.plot(x, y, 'black')
    plt.xlabel('Radius')
    plt.ylabel('Density')
    plt.show()


# assuming that the initial run-time is 1, and there are 49,999 time steps
def plot_density_heat_map(density, central, desired_time):

    time_step = math.floor(len(density) * desired_time)

    phi = density[time_step]
    c_phi = central[time_step]

    radial_values = np.arange(0, len(density[0]) + 1)
    angular_values = np.linspace(0, 2 * np.pi, len(density[0][0]))

    phi_with_center = np.zeros((len(density[0] + 1), len(density[0][0])))
    phi_with_center[0, :] = c_phi
    phi_with_center[1:, :] = phi

    norm = Normalize(vmin=phi_with_center.min(), vmax=phi_with_center.max())
    phi_normalized = norm(phi_with_center)

    r, theta = np.meshgrid(radial_values, angular_values)

    plt.figure()
    ax = plt.subplot(projection='polar')

    c = ax.pcolormesh(theta, r, shading='auto', cmap='viridis')
    # c = ax.pcolormesh(theta, r, phi_normalized.T, shading='auto', cmap='viridis')

    plt.colorbar(c, label='Normalized Density')

    plt.title(f'Density Distribution at time step {time_step}')
    plt.xlabel('Angle')
    plt.ylabel('Radius')
    plt.show()


def plot_density_heat_map_discrete(density, central, time_step):

    phi = density[time_step]
    c_phi = central[time_step]
    # c_phi = 0

    radial_values = np.arange(0, len(density[0]) + 1)
    angular_values = np.linspace(0, 2 * np.pi, len(density[0][0]))

    phi_with_center = np.zeros((len(density[0]) + 1, len(density[0][0])))
    phi_with_center[0, :] = c_phi
    phi_with_center[1:, :] = phi

    norm = Normalize(vmin=phi_with_center.min(), vmax=phi_with_center.max())
    phi_normalized = norm(phi_with_center)

    r, theta = np.meshgrid(radial_values, angular_values)

    plt.figure()
    ax = plt.subplot(projection='polar')

    c = ax.pcolormesh(theta, r, phi_normalized.T, shading='auto', cmap='viridis')

    plt.colorbar(c, label='Normalized Density Legend')

    plt.title(f'Density Distribution at time step {time_step}')
    plt.xlabel('Angle')
    plt.ylabel('Radius')
    plt.show()


def plot_density_heat_map_discrete_animated(density, central, time_step_bound):
    num_radial_curves = len(density[0])
    num_angles = len(density[0][0])

    radial_values = np.linspace(0, 1, num_radial_curves + 1)
    angular_values = np.linspace(0, 2 * np.pi, num_angles, endpoint=False)

    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

    r, theta = np.meshgrid(radial_values, angular_values)
    phi_with_center = np.zeros((num_angles, num_radial_curves + 1))
    c = ax.pcolormesh(theta, r, phi_with_center, shading='auto', cmap='viridis')

    plt.colorbar(c, ax=ax, label='Normalized Density')

    # Set radial ticks
    ax.set_rticks(radial_values)
    ax.set_rlabel_position(-22.5)

    # Set angular ticks
    ax.set_xticks(np.linspace(0, 2 * np.pi, num_angles, endpoint=False))

    ax.grid(True)

    norm = Normalize(vmin=density.min(), vmax=density.max())  # Normalize over the entire dataset

    def update(frame):
        phi = density[frame]
        c_phi = central[frame]

        phi_with_center[:, 0] = c_phi
        phi_with_center[:, 1:] = phi.T

        c.set_array(norm(phi_with_center).ravel())
        return c,

    ani = FuncAnimation(fig, update, frames=range(time_step_bound), blit=True, repeat=False)
    plt.show()