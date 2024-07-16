import math
import print_functions as pr
import numpy as np


# update density
def u_density(phi, k, m, n, d_radius, d_theta, d_time, central, rings):

    curr_density = phi[k][m][n]

    component_a = ((m+2) * j_r_r(phi, k, m, n, d_radius, rings)) - ((m+1) * j_l_r(phi, k, m, n, d_radius, central))
    component_a *= d_time / ((m+1) * d_radius)

    component_b = (j_r_t(phi, k, m, n, d_radius, d_theta)) - (j_l_t(phi, k, m, n, d_radius, d_theta))
    component_b *= d_time / ((m+1) * d_radius * d_theta)

    return curr_density - component_a - component_b


# update central density
def u_center(phi, k, d_radius, d_theta, d_time, curr_central):
    total_sum = 0
    for n in range(len(phi[k][0])):
        total_sum += j_l_r(phi, k, 0, n, d_radius, curr_central)
    total_sum *= (d_theta * d_time) / (math.pi * d_radius)
    return curr_central - total_sum


# calculate for total mass
def calc_mass(phi, k, d_radius, d_theta, curr_central, rings, rays):
    mass = 0
    for m in range(rings):
        for n in range(rays):
            mass += phi[k][m][n] * (m+1)
    mass *= (d_radius * d_radius) * d_theta
    return (curr_central * math.pi * d_radius * d_radius) + mass


def calc_loss_mass_j(phi, k, d_radius, d_theta, rings, rays):
    total_sum = 0
    for n in range(rays):
        total_sum += j_r_r(phi, k, rings-2, n, d_radius, 0)
    total_sum *= rings * d_radius * d_theta

    return total_sum


# This should be calculated after the solution algorithm has successfully executed
# def calc_loss_mass_derivative(mass_container, d_time):
#     array = np.zeros([len(mass_container)-1])
#
#     for k in range(len(mass_container) - 1):
#         array[k] = (mass_container[k] - mass_container[k+1])/d_time
#
#     return array

def calc_loss_mass_derivative(mass_container, d_time):
    array = np.zeros([len(mass_container) - 1])
    for k in range(1, len(mass_container)):
        array[k-1] = (mass_container[k-1] - mass_container[k]) / d_time
    return array


# def calc_loss_mass_derivative(mass_container, d_time):
#     array = np.zeros([len(mass_container) - 1])
#     for k in range(1, len(mass_container) - 1):
#         array[k-1] = (mass_container[k-1] - mass_container[k+1]) / (2 * d_time)
#     return array


def calculate_total_mass(phi, k, radial_curves, angular_rays, center, d_radius, d_theta):
    total_sum = 0
    for m in range(radial_curves):
        for n in range(angular_rays):
            total_sum += phi[k][m] * (m + 1)
    total_sum *= (d_radius * d_radius) * d_theta
    return (center * math.pi * d_radius * d_radius) + total_sum


# J Right Radius
def j_r_r(phi, k, m, n, d_radius, rings):
    curr_ring = phi[k][m][n]
    if m + 1 == rings - 1:
        next_ring = 0
    else:
        next_ring = phi[k][m+1][n]
    return -1 * ((next_ring - curr_ring) / d_radius)


# J Left Radius
def j_l_r(phi, k, m, n, d_radius, central):
    curr_ring = phi[k][m][n]
    if m == 0:
        prev_ring = central
    else:
        prev_ring = phi[k][m-1][n]
    return -1 * ((curr_ring - prev_ring) / d_radius)


# J Right Theta
def j_r_t(phi, k, m, n, d_radius, d_theta):
    b = len(phi[k][m])
    return -1 * (phi[k][m][(n+1) % b] - phi[k][m][n]) / ((m+1) * d_radius * d_theta)


# J Left Theta
def j_l_t(phi, k, m, n, d_radius, d_theta):
    b = len(phi[k][m])
    return -1 * (phi[k][m][n] - phi[k][m][(n-1) % b]) / ((m+1) * d_radius * d_theta)


'''
rings   = Radial curves 
rays    = Angular rays
r       = Domain radius
d       = Diffusion coefficient
t       = Run time
q       = Passing a boolean value to determine if the user would like to print initial quantities
p       = Progression frequency for print operations
'''


# computing the underlying solution
def solve(rings, rays, r, d, t, q, p):

    d_radius = r / rings
    d_theta = (2 * math.pi) / rays
    d_time = (0.1 * min(d_radius * d_radius, d_theta * d_radius)) / (2 * d)
    time_steps = math.ceil(t / d_time)
    phi_center = 1 / (math.pi * (d_radius * d_radius))

    if q:
        pr.pr_quantities(rings, rays, r, d, t, d_radius, d_theta, d_time, time_steps, phi_center)

    phi_tab = np.zeros([time_steps + 1, rings, rays])
    central_phi_tab = np.zeros([time_steps])
    mass_tab = np.zeros([time_steps])
    mass_loss_tab = np.zeros([time_steps])

    for k in range(time_steps):
        if q:
            if k % p == 0:
                pr.pr_progress(k, time_steps)

        for m in range(rings):
            if m == rings - 2:
                mass_loss_tab[k] = calc_loss_mass_j(phi_tab, k, d_radius, d_theta, rings, rays)
            for n in range(rays):
                if m == rings - 1:
                    phi_tab[k+1][m][n] = 0
                else:
                    phi_tab[k+1][m][n] = u_density(phi_tab, k, m, n, d_radius, d_theta, d_time, phi_center, rings)

        central_phi_tab[k] = phi_center

        mass_tab[k] = calc_mass(phi_tab, k, d_radius, d_theta, phi_center, rings, rays)
        phi_center = u_center(phi_tab, k, d_radius, d_theta, d_time, phi_center)

    mass_loss_tab_ii = calc_loss_mass_derivative(mass_tab, d_time)

    print()
    if q:
        print('Successful Completion.')
    return phi_tab, central_phi_tab, mass_tab, mass_loss_tab, mass_loss_tab_ii, d_time














