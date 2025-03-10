# Import statements
from matplotlib import pyplot as plt
from tudatpy.kernel import numerical_simulation
from tudatpy.kernel.astro import element_conversion, time_conversion
from tudatpy.kernel.astro.fundamentals import compute_shadow_function
from tudatpy.kernel.interface import spice
from tudatpy.kernel.numerical_simulation import environment_setup, propagation_setup
from tudatpy.util import result2array

from useful_functions import *

# Initial settings (independent of tudat)
orbit_name = 'SSO6'
dates_name = '5days_1min'
spacecraft_name = 'Tolosat'
groundstation_name = 'toulouse'

# Load spice kernels
spice.load_standard_kernels([])

# Set simulation start and end epochs (in seconds since J2000 = January 1, 2000 at 00:00:00)
dates = get_dates(dates_name)
simulation_start_epoch = time_conversion.julian_day_to_seconds_since_epoch(
    time_conversion.calendar_date_to_julian_day(dates["start_date"]))
simulation_end_epoch = time_conversion.julian_day_to_seconds_since_epoch(
    time_conversion.calendar_date_to_julian_day(dates["end_date"]))

# Create default body settings and bodies system
bodies_to_create = ["Earth", "Sun", "Moon", "Jupiter"]
global_frame_origin = "Earth"
global_frame_orientation = "J2000"
body_settings = environment_setup.get_default_body_settings(
    bodies_to_create, global_frame_origin, global_frame_orientation)
bodies = environment_setup.create_system_of_bodies(body_settings)

# Add vehicle object to system of bodies
bodies.create_empty_body("Tolosat")
bodies.get("Tolosat").mass = get_spacecraft(spacecraft_name)["mass"]

# Create aerodynamic coefficient interface settings, and add to vehicle
reference_area = get_spacecraft(spacecraft_name)["drag_area"]
drag_coefficient = get_spacecraft(spacecraft_name)["drag_coefficient"]
aero_coefficient_settings = environment_setup.aerodynamic_coefficients.constant(
    reference_area, [drag_coefficient, 0, 0]
)
environment_setup.add_aerodynamic_coefficient_interface(
    bodies, "Tolosat", aero_coefficient_settings)

# Create radiation pressure settings, and add to vehicle
reference_area_radiation = get_spacecraft(spacecraft_name)["srp_area"]
radiation_pressure_coefficient = get_spacecraft(spacecraft_name)["reflectivity_coefficient"]
occulting_bodies = ["Earth"]
radiation_pressure_settings = environment_setup.radiation_pressure.cannonball(
    "Sun", reference_area_radiation, radiation_pressure_coefficient, occulting_bodies
)
environment_setup.add_radiation_pressure_interface(
    bodies, "Tolosat", radiation_pressure_settings)

# Define bodies that are propagated and their respective central bodies
bodies_to_propagate = ["Tolosat"]
central_bodies = ["Earth"]

# Define accelerations acting on the spacecraft
acceleration_settings_spacecraft = dict(
    Sun=[
        propagation_setup.acceleration.cannonball_radiation_pressure(),
        propagation_setup.acceleration.point_mass_gravity()
    ],
    Earth=[
        propagation_setup.acceleration.spherical_harmonic_gravity(12, 12),
        propagation_setup.acceleration.aerodynamic()
    ],
    Moon=[
        propagation_setup.acceleration.point_mass_gravity()
    ],
    Jupiter=[
        propagation_setup.acceleration.point_mass_gravity()
    ]
)

acceleration_settings = {"Tolosat": acceleration_settings_spacecraft}

# Create acceleration models
acceleration_models = propagation_setup.create_acceleration_models(
    bodies, acceleration_settings, bodies_to_propagate, central_bodies
)

# Set initial conditions for the satellite
earth_gravitational_parameter = bodies.get("Earth").gravitational_parameter
orbit = get_orbit(orbit_name)
initial_state = element_conversion.keplerian_to_cartesian_elementwise(
    gravitational_parameter=earth_gravitational_parameter,
    semi_major_axis=orbit["semi_major_axis"],
    eccentricity=orbit["eccentricity"],
    inclination=np.deg2rad(orbit["inclination"]),
    argument_of_periapsis=np.deg2rad(orbit["argument_of_periapsis"]),
    longitude_of_ascending_node=np.deg2rad(orbit["longitude_of_ascending_node"]),
    true_anomaly=np.deg2rad(orbit["true_anomaly"]),
)

# Setup dependent variables to be save
sun_position_dep_var = propagation_setup.dependent_variable.relative_position("Sun", "Earth")
earth_position_dep_var = propagation_setup.dependent_variable.relative_position("Earth", "Earth")
keplerian_states_dep_var = propagation_setup.dependent_variable.keplerian_state("Tolosat", "Earth")
ecef_pos_dep_var = propagation_setup.dependent_variable.central_body_fixed_cartesian_position("Tolosat", "Earth")
dependent_variables_to_save = [sun_position_dep_var, earth_position_dep_var, keplerian_states_dep_var, ecef_pos_dep_var]

# Create termination settings
termination_condition = propagation_setup.propagator.time_termination(simulation_end_epoch)

# Create propagation settings
propagator_settings = propagation_setup.propagator.translational(
    central_bodies,
    acceleration_models,
    bodies_to_propagate,
    initial_state,
    termination_condition,
    output_variables=dependent_variables_to_save
)

# Create numerical integrator settings
fixed_step_size = dates["step_size"].total_seconds()
integrator_settings = propagation_setup.integrator.runge_kutta_4(
    simulation_start_epoch, fixed_step_size
)

# Create simulation object and propagate the dynamics
dynamics_simulator = numerical_simulation.SingleArcSimulator(
    bodies, integrator_settings, propagator_settings
)

# Extract the resulting state history and convert it to a ndarray
states = dynamics_simulator.state_history
states_array = result2array(states)
dependent_variables_history = dynamics_simulator.dependent_variable_history
dependent_variables_history_array = result2array(dependent_variables_history)

sun_radius = bodies.get("Sun").shape_model.average_radius
earth_radius = bodies.get("Earth").shape_model.average_radius
states_array[:, 0] = states_array[:, 0] - states_array[0, 0]
satellite_position = states_array[:, 1:4]
sun_position = dependent_variables_history_array[:, 1:4]
earth_position = dependent_variables_history_array[:, 4:7]
keplerian_states = dependent_variables_history_array[:, 7:13]
ecef_position = dependent_variables_history_array[:, 13:16]

satellite_shadow_function = np.empty(len(satellite_position))
satellite_shadow_function[:] = np.NaN

for ii in range(len(satellite_position)):
    satellite_shadow_function[ii] = compute_shadow_function(sun_position[ii], sun_radius, earth_position[ii],
                                                            earth_radius, satellite_position[ii])

groundstation = get_station(groundstation_name)
visibility, elevation = compute_visibility(ecef_position, groundstation)

satellite_lla = ecf2lla(ecef_position)

# Export results to a CSV file
# write_results(spacecraft_name, orbit_name, dates_name,
#               np.concatenate((states_array, keplerian_states, ecef_position), axis=1))

# Create a static 3D figure of the trajectory
fig = plt.figure(figsize=(7, 5.2), dpi=500)
ax = fig.add_subplot(111, projection='3d')
ax.set_title(f'Spacecraft trajectory around the Earth')
ax.plot(states_array[:, 1] / 1E3, states_array[:, 2] / 1E3, states_array[:, 3] / 1E3, label=bodies_to_propagate[0],
        linestyle='-.')
plot_sphere(ax, [0, 0, 0], earth_radius / 1E3)

# Add the legend and labels, then show the plot
ax.legend()
ax.set_xlabel('x [km]')
ax.set_ylabel('y [km]')
ax.set_zlabel('z [km]')
plt.savefig(f'results/{spacecraft_name}_{orbit_name}_{dates_name}.png')
plt.show()

# Plot the shadow function
fig = plt.figure(figsize=(7, 5.2), dpi=500)
ax = fig.add_subplot(111)
ax.set_title(f'Spacecraft shadow function')
ax.plot((states_array[:, 0] - states_array[0, 0]) / 3600, satellite_shadow_function, label=bodies_to_propagate[0],
        linestyle='-')
ax.set(xlabel='Time [h]', ylabel='Shadow function')
plt.savefig(f'results/{spacecraft_name}_{orbit_name}_{dates_name}_shadow_function.png')
plt.show()

# Plot the visibility function
fig = plt.figure(figsize=(7, 5.2), dpi=500)
ax = fig.add_subplot(111)
ax.set_title(f'Spacecraft ground station visibility function')
ax.plot((states_array[:, 0] - states_array[0, 0]) / 3600, visibility, label=bodies_to_propagate[0],
        linestyle='-')
ax.set(xlabel='Time [h]', ylabel='Visibility function')
plt.savefig(f'results/{spacecraft_name}_{orbit_name}_{dates_name}_visibility_function.png')
plt.show()

# Write an interactive HTML visualization of the trajectory
fig = plotly_trajectory(states_array[:, 0], states_array[:, 1] / 1E3, states_array[:, 2] / 1E3,
                        states_array[:, 3] / 1E3)
finish_plotly_figure(fig, f'results/{spacecraft_name}_{orbit_name}_{dates_name}_trajectory.html')


