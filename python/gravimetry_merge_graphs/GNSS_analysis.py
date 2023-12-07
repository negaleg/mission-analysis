import matplotlib.pyplot as plt

def plots(option):
    # Import data based on the selected option
    if option == 1 or option == 2 or option == 4:
        from gravimetry.gps_doppler import gps_sat_results, gps_visibility, gps_windows
    if option == 2 or option == 3 or option == 4:
        from gravimetry_glonass.glonass_doppler import glonass_sat_results, glonass_visibility, glonass_windows
    if option == 1 or option == 3 or option == 4:
        from gravimetry_galileo.galileo_doppler import galileo_sat_results, galileo_visibility, galileo_windows

    # Doppler shift plot
    plt.figure(figsize=(10, 5))
    # Plot Doppler rate for GPS with blue color
    gps_line = None
    if option == 1 or option == 2 or option == 4:
        gps_line, = plt.plot(gps_sat_results["seconds"] / 86400, gps_sat_results["doppler_shift"] / 1e3, label="GPS",
                             color="blue")
    # Plot Doppler shift for GLONASS with orange color
    glonass_line = None
    if option == 2 or option == 3 or option == 4:
        glonass_line, = plt.plot(glonass_sat_results["seconds"] / 86400, glonass_sat_results["doppler_shift"] / 1e3,
                                     label="GLONASS", color="orange")
    # Plot Doppler shift for Galileo with green color
    galileo_line = None
    if option == 1 or option == 3 or option == 4:
        galileo_line, = plt.plot(galileo_sat_results["seconds"] / 86400, galileo_sat_results["doppler_shift"] / 1e3,
                                     label="Galileo", color="green")
    # Create legend only if there are labeled artists
    if gps_line or glonass_line or galileo_line:
        plt.legend()

    plt.title("Doppler Shift Comparison")
    plt.xlabel("Time since launch [days]")
    plt.ylabel("Doppler shift [kHz]")
    plt.grid(True)
    plt.show()

    # Doppler rate plot
    plt.figure(figsize=(10, 5))
    # Plot Doppler rate for GPS with blue color
    gps_line = None
    if option == 1 or option == 2 or option == 4:
        gps_line, = plt.plot(gps_sat_results["seconds"] / 86400, gps_sat_results["doppler_rate"], label="GPS",
                             color="blue")
    # Plot Doppler rate for GLONASS with orange color
    glonass_line = None
    if option == 2 or option == 3 or option == 4:
        glonass_line, = plt.plot(glonass_sat_results["seconds"] / 86400, glonass_sat_results["doppler_rate"],
                                     label="GLONASS", color="orange")
    # Plot Doppler rate for Galileo with green color
    galileo_line = None
    if option == 1 or option == 3 or option == 4:
        galileo_line, = plt.plot(galileo_sat_results["seconds"] / 86400, galileo_sat_results["doppler_rate"],
                                     label="Galileo", color="green")
    # Create legend only if there are labeled artists
    if gps_line or glonass_line or galileo_line:
        plt.legend()

    plt.title("Doppler Rate Comparison")
    plt.xlabel("Time since launch [days]")
    plt.ylabel("Doppler rate [Hz/s]")
    plt.grid(True)
    plt.show()

    # Visibility of the satellites satisfying all 5 conditions
    plt.figure(figsize=(10, 5))
    # Plot visibility for GPS with blue color
    gps_line = None
    if option == 1 or option == 2 or option == 4:
        gps_line, = plt.plot(gps_visibility["seconds"] / 86400, gps_visibility["sum_ok"], linestyle="none",
                                    marker=".", label="GPS", color="blue")
    # Plot visibility for GLONASS with orange color
    glonass_line = None
    if option == 2 or option == 3 or option == 4:
        glonass_line, = plt.plot(glonass_visibility["seconds"] / 86400, glonass_visibility["sum_ok"], linestyle="none",
                                     marker=".", label="GLONASS", color="orange")
    # Plot visibility for Galileo with green color
    galileo_line = None
    if option == 1 or option == 3 or option == 4:
        galileo_line, = plt.plot(galileo_visibility["seconds"] / 86400, galileo_visibility["sum_ok"], linestyle="none",
                                    marker=".", label="Galileo", color="green")
    # Create legend only if there are labeled artists
    if gps_line or glonass_line or galileo_line:
        plt.legend()

    plt.title("Visibility of GNSS satellites satisfying all 5 conditions")
    plt.xlabel("Time since launch [days]")
    plt.ylabel("Number of satellites [-]")
    plt.grid(True)
    plt.show()

    # Visibility windows of at least one GNSS satellite
    plt.figure(figsize=(10, 5))
    # Plot visibility windows for GPS with blue color
    gps_line = None
    if option == 1 or option == 2 or option == 4:
        gps_line, = plt.vlines(gps_windows["seconds"] / 86400, 0, gps_windows["duration"] / 60, label="GPS", color="blue")
    # Plot visibility windows for GLONASS with orange color
    glonass_line = None
    if option == 2 or option == 3 or option == 4:
        glonass_line, = plt.vlines(glonass_windows["seconds"] / 86400, 0, glonass_windows["duration"] / 60,
                                   label="GLONASS", color="orange")
    # Plot visibility windows for Galileo with green color
    galileo_line = None
    if option == 1 or option == 3 or option == 4:
        galileo_line, = plt.vlines(galileo_windows["seconds"] / 86400, 0, galileo_windows["duration"] / 60,
                                   label="Galileo", color="green")
    # Create legend only if there are labeled artists
    if gps_line or glonass_line or galileo_line:
            plt.legend()

    plt.title("Visibility windows of at least one GNSS satellite")
    plt.xlabel("Time since launch [days]")
    plt.ylabel("Window duration [mins]")
    plt.grid(True)
    plt.show()


# Select an option to merge the graphs:
# 1: GPS and Galileo
# 2: GPS and Glonass
# 3: Galileo and Glonass
# 4: GPS Galileo and Glonass
option = 4
plots(option)


