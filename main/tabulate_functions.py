import pandas as pd
import numpy as np
from datetime import datetime
import os


def tabulate_mass(container, filepath, time, delta_time):
    # time_steps = np.linspace(0, time, len(container))
    time_steps = [ k * delta_time for k in range(1, len(container) + 1) ]

    df = pd.DataFrame({'T': time_steps, 'M': container})

    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"mass_data_{current_time}_{time}.csv"

    if not os.path.exists(filepath):
        os.makedirs(filepath)

    df.to_csv(os.path.join(filepath, filename), sep=',', index=False)


def tabulate_mass_loss(container, filepath, time, delta_time):

    # time_steps = np.linspace(0, time, len(container))
    time_steps = [k * delta_time for k in range(1, len(container) + 1)]

    df = pd.DataFrame({'T': time_steps, 'M': container})

    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"mass_loss_data_{current_time}_{time}.csv"

    if not os.path.exists(filepath):
        os.makedirs(filepath)

    df.to_csv(os.path.join(filepath, filename), sep=',', index=False)


def tabulate_central(container, filepath, time, delta_time):
    # time_steps = np.linspace(0, time, len(container))
    time_steps = [ k * delta_time for k in range(1, len(container) + 1) ]

    df = pd.DataFrame({'T': time_steps, 'M': container})
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"center_density_data_{current_time}_{time}.csv"

    if not os.path.exists(filepath):
        os.makedirs(filepath)

    df.to_csv(os.path.join(filepath, filename), sep=',', index=False)


def tabulate_densities(container, filepath, radius, angle, time):
    final_state = container[len(container)-1]

    radial_steps = np.linspace(0, radius, len(container[0][0]))
    radial_densities = np.zeros([len(container[0][0])])

    for i in range(len(final_state)):
        radial_densities[i] = final_state[i][angle]

    df = pd.DataFrame({'R': radial_steps, 'D': radial_densities})

    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"density_across_radius_data_{current_time}_{time}.csv"

    if not os.path.exists(filepath):
        os.makedirs(filepath)

    df.to_csv(os.path.join(filepath, filename), sep=',', index=False)


