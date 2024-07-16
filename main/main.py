import calc
import tabulate_functions as tb
import plot_functions as plt
from playsound import playsound

if __name__ == "__main__":

    rings = 50
    rays = 50
    # Diffusion coefficient
    d = 1
    # Domain Radius
    r = 1
    # Run time
    t = 1

    density_table, center_table, mass_table, mass_loss_i, mass_loss_ii, delta_time = calc.solve(rings, rays, r, d, t, True, 1)

    print(f'Size of container: {len(density_table)}')

    tb.tabulate_mass(mass_table, mass_data_filepath, t, delta_time)
    tb.tabulate_central(center_table, central_densities_filepath, t, delta_time)
    tb.tabulate_densities(density_table, domain_density_filepath, r, 0, t)
    tb.tabulate_mass_loss(mass_loss_i, mass_loss_data_filepath, t, delta_time)
    # tb.tabulate_mass_loss(mass_loss_ii, mass_loss_data_filepath, t)

    # plt.plot_mass(mass_table, t)
    # plt.plot_central_density(center_table, t)
    # plt.plot_final_density(density_table, r, 0)
    # plt.plot_all_densities(density_table, r, 0, 4000)
    # plt.plot_mass_loss(mass_loss_i, t)
    # plt.plot_mass_loss(mass_loss_ii, t)
    # plt.plot_moss_loss_comparison(mass_loss_i, mass_loss_ii, t)
    # plt.plot_density_heat_map_discrete_animated(density_table, center_table, len(density_table))

    # plt.plot_density_heat_map_discrete(density_table, center_table, time_step)
    # plt.plot_density_heat_map_discrete_animated(density_table, center_table, len(density_table))
