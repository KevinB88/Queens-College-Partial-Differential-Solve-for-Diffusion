import sys


def pr_quantities(rings, rays, r, d, t, d_radius, d_theta, d_time, time_steps, phi_center):
    print(f'Radial Curves: {rings}')
    print(f'Angular Rays: {rays}')
    print(f'Domain Radius: {r}')
    print(f'Diffusion Coefficient: {d}')
    print(f'Run Time: {t}')
    print(f'Delta Radius: {d_radius}')
    print(f'Delta Theta: {d_theta}')
    print(f'Delta Time: {d_time}')
    print(f'Time steps: {time_steps}')
    print(f'Initial Central Density: {phi_center}')
    print()


def pr_progress(c, o):
    percent = (c / o) * 100
    print(f"\rProgress: {int(percent+1)}%", end='', flush=True)

