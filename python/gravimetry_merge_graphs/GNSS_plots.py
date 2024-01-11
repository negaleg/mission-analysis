#import matplotlib.pyplot as plt
import pandas as pd
from useful_functions import plot_functions as pf

def plots(option):
    # Import data based on the selected option
    if option == 1 or option == 2 or option == 4:
        from gravimetry.gps_doppler import gps_sat_results, gps_visibility, gps_windows, selected_gps, selected_gps_nospace
    if option == 2 or option == 3 or option == 4:
        from gravimetry_glonass.glonass_doppler import glonass_sat_results, glonass_visibility, glonass_windows, selected_glonass, selected_glonass_nospace
    if option == 1 or option == 3 or option == 4:
        from gravimetry_galileo.galileo_doppler import galileo_sat_results, galileo_visibility, galileo_windows, selected_galileo, selected_galileo_nospace

    if option == 1:
        combined_sat_results = pd.concat([gps_sat_results, galileo_sat_results], ignore_index=True)
        combined_visibility = pd.concat([gps_visibility, galileo_visibility], ignore_index=True)
        combined_windows = pd.concat([gps_windows, galileo_windows], ignore_index=True)
        selected_combined = selected_gps + " " + selected_galileo
        selected_combined_nospace = selected_gps_nospace + "_" + selected_galileo_nospace
    if option == 2:
        combined_sat_results = pd.concat([gps_sat_results, glonass_sat_results], ignore_index=True)
        combined_visibility = pd.concat([gps_visibility, glonass_visibility], ignore_index=True)
        combined_windows = pd.concat([gps_windows, glonass_windows], ignore_index=True)
        selected_combined = selected_gps + " " + selected_glonass
        selected_combined_nospace = selected_gps_nospace + "_" + selected_glonass_nospace
    if option == 3:
        combined_sat_results = pd.concat([glonass_sat_results, galileo_sat_results], ignore_index=True)
        combined_visibility = pd.concat([glonass_visibility, galileo_visibility], ignore_index=True)
        combined_windows = pd.concat([glonass_windows, galileo_windows], ignore_index=True)
        selected_combined = selected_glonass + " " + selected_galileo
        selected_combined_nospace = selected_glonass_nospace + "_" + selected_galileo_nospace
    if option == 4:
        combined_sat_results = pd.concat([gps_sat_results, galileo_sat_results, glonass_sat_results], ignore_index=True)
        combined_visibility = pd.concat([gps_visibility, galileo_visibility, glonass_visibility], ignore_index=True)
        combined_windows = pd.concat([gps_windows, galileo_windows, glonass_windows], ignore_index=True)
        selected_combined = selected_gps + " " + selected_galileo + " " + selected_glonass
        selected_combined_nospace = selected_gps_nospace + "_" + selected_galileo_nospace + "_" + selected_glonass_nospace

    # Doppler shift dark
    fig, axes = pf.dark_figure()
    axes[0].plot(combined_sat_results["seconds"] / 86400, combined_sat_results["doppler_shift"] / 1e3)
    axes[0].set_title(f"Doppler shift of {selected_combined}")
    axes[0].set_xlabel("Time since launch [days]")
    axes[0].set_ylabel("Doppler shift [kHz]")
    axes[0].set_xlim(0, combined_sat_results["seconds"].max() / 86400)
    pf.finish_dark_figure(
        fig, f"results/{selected_combined_nospace}_doppler_shift.png", show=True
    )

    # Doppler shift light
    fig, axes = pf.light_figure()
    axes[0].plot(combined_sat_results["seconds"] / 86400, combined_sat_results["doppler_shift"] / 1e3)
    axes[0].set_title(f"Doppler shift of {selected_combined}")
    axes[0].set_xlabel("Time since launch [days]")
    axes[0].set_ylabel("Doppler shift [kHz]")
    axes[0].set_xlim(0, combined_sat_results["seconds"].max() / 86400)
    pf.finish_light_figure(
        fig, f"results/{selected_combined_nospace}_doppler_shift_light.png", show=True
    )

    # Doppler rate dark
    fig, axes = pf.dark_figure()
    axes[0].plot(combined_sat_results["seconds"] / 86400, combined_sat_results["doppler_rate"])
    axes[0].set_title(f"Doppler rate of {selected_gps}")
    axes[0].set_xlabel("Time since launch [days]")
    axes[0].set_ylabel("Doppler rate [Hz/s]")
    axes[0].set_xlim(0, combined_sat_results["seconds"].max() / 86400)
    pf.finish_dark_figure(
        fig, f"results/{selected_combined_nospace}_doppler_rate.png", show=True
    )

    # Doppler rate light
    fig, axes = pf.light_figure()
    axes[0].plot(combined_sat_results["seconds"] / 86400, combined_sat_results["doppler_rate"])
    axes[0].set_title(f"Doppler rate of {selected_combined}")
    axes[0].set_xlabel("Time since launch [days]")
    axes[0].set_ylabel("Doppler rate [Hz/s]")
    axes[0].set_xlim(0, combined_sat_results["seconds"].max() / 86400)
    pf.finish_light_figure(
        fig, f"results/{selected_combined_nospace}_doppler_rate_light.png", show=True
    )


    # Visibility of the satellites satisfying all 5 conditions dark figure
    fig, axes = pf.dark_figure()
    axes[0].plot(
        combined_visibility["seconds"] / 86400,
        combined_visibility["sum_ok"],
        linestyle="none",
        marker=".",
    )
    axes[0].set_title("Visibility of GNSS satellites satisfying all 5 conditions")
    axes[0].set_xlabel("Time since launch [days]")
    axes[0].set_ylabel("Number of satellites [-]")
    axes[0].set_xlim(0, gps_visibility["seconds"].max() / 86400)
    pf.finish_dark_figure(fig, "results/combined_visibility.png", show=True, force_y_int=True)

    # Visibility of the satellites satisfying all 5 conditions light figure
    fig, axes = pf.light_figure()
    axes[0].plot(
        combined_visibility["seconds"] / 86400,
        combined_visibility["sum_ok"],
        linestyle="none",
        marker=".",
    )
    axes[0].set_title("Visibility of GNSS satellites satisfying all 5 conditions")
    axes[0].set_xlabel("Time since launch [days]")
    axes[0].set_ylabel("Number of satellites [-]")
    axes[0].set_xlim(0, combined_visibility["seconds"].max() / 86400)
    pf.finish_light_figure(
        fig, "results/combined_visibility_light.png", show=True, force_y_int=True
    )

    # Window duration dark
    fig, axes = pf.dark_figure()
    axes[0].vlines(combined_windows["seconds"] / 86400, 0, combined_windows["duration"] / 60)
    axes[0].set_title("Visibility windows of at least one GNSS satellite")
    axes[0].set_xlabel("Time since launch [days]")
    axes[0].set_ylabel("Window duration [mins]")
    axes[0].set_ylim(0, combined_windows["duration"].max() / 60)
    axes[0].set_xlim(0, combined_windows["seconds"].max() / 86400)
    pf.finish_dark_figure(fig, "results/combined_windows.png", show=True)

    # Window duration light
    fig, axes = pf.light_figure()
    axes[0].vlines(combined_windows["seconds"] / 86400, 0, combined_windows["duration"] / 60)
    axes[0].set_title("Visibility windows of at least one GNSS satellite")
    axes[0].set_xlabel("Time since launch [days]")
    axes[0].set_ylabel("Window duration [mins]")
    axes[0].set_ylim(0, combined_windows["duration"].max() / 60)
    axes[0].set_xlim(0, combined_windows["seconds"].max() / 86400)
    pf.finish_light_figure(fig, "results/combined_windows_light.png", show=True)

# Select an option to merge the graphs:
# 1: GPS and Galileo
# 2: GPS and Glonass
# 3: Galileo and Glonass
# 4: GPS Galileo and Glonass
option = 4
plots(option)