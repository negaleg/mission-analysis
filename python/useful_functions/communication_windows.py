from datetime import timedelta, datetime
from typing import Dict

import numpy as np
import pandas as pd
from pyproj import Transformer
from tudatpy.kernel.astro import time_conversion
from tudatpy.kernel.astro.time_conversion import julian_day_to_calendar_date, seconds_since_epoch_to_julian_day
from useful_functions import get_input_data



def compute_visibility(pos_ecf, station, dates_name):
    """
    Compute the visibility of the spacecraft from a given ground station.

    Parameters
    ----------
    pos_ecf : ndarray
        Array of satellite positions in ECIframe
    station : dict
        Dictionary containing longitude, latitude, altitude, and minimum elevation of the groundstation
    dates_name : string
        String of the name of a csv file containing the start date, the end date, and the step size of the simulation

    Returns
    -------
    visibility : ndarray
        Returns a vector with the value of the visibility at each epoch :
         - False if there is no communication between the satellite and the ground station
         - True if there is communication between the satellite and the ground station

    elevation : ndarray
        Returns a vector containing the elevation angle between the satellite and the ground station

    time : ndarray
        Returns a vector containing the time in calendar date

    communication_windows: dataframe
        Returns a data frame containing the following information about the communication windows
         - 'time'                   : time in calendar date
         - 'visibility'             : boolean on state of visibility
         - 'start_of_streak'        : boolean which is 'True' if it is the start of a communication window
                                        or a no-communication window, 'False' if not
         - 'streak_id'              : integer that sequentially unequivocally identifies the communication window
                                        or a no-communication window
         - 'streak_counter'         : integer that identifies the elements of a single communication window
                                        or a no-communication window
         - 'streak_counter_seconds' : elapsed time in seconds since the start of a communication window
                                        or a no-communication window
    """
    transformer = Transformer.from_crs(
        {"proj": 'latlong', "ellps": 'WGS84', "datum": 'WGS84'},
        {"proj": 'geocent', "ellps": 'WGS84', "datum": 'WGS84'},
    )
    # Set simulation start and end epochs (in seconds since J2000 = January 1, 2000 at 00:00:00)
    dates: dict[str, timedelta | datetime] = get_input_data.get_dates(dates_name)
    dates_new = get_input_data.get_dates(dates_name)  # calendar date
    simulation_start_epoch = time_conversion.julian_day_to_seconds_since_epoch(
        time_conversion.calendar_date_to_julian_day(dates_new["start_date"])) #seconds since epoch
    simulation_end_epoch = time_conversion.julian_day_to_seconds_since_epoch(
        time_conversion.calendar_date_to_julian_day(dates_new["end_date"])) #seconds since epoch
    simulation_step_epoch = dates_new["step_size"].seconds  # seconds
    tm = np.arange(simulation_start_epoch, simulation_end_epoch + simulation_step_epoch, simulation_step_epoch)
    time=[]
    for i in tm:
        time.append(time_conversion.julian_day_to_calendar_date(time_conversion.seconds_since_epoch_to_julian_day(i))) #calendar date

    station_ecf = transformer.transform(station["longitude"], station["latitude"], station["altitude"], radians=False)
    station_sat_vector = pos_ecf - station_ecf
    station_ecf_unit = station_ecf / np.linalg.norm(station_ecf)
    station_sat_vector_unit = station_sat_vector.T / np.apply_along_axis(np.linalg.norm, 1, station_sat_vector)
    dot_product = np.dot(station_ecf_unit, station_sat_vector_unit)
    elevation = 90 - np.arccos(dot_product) * 180 / np.pi
    visibility = elevation >= station["minimum_elevation"]

    communication_windows = pd.DataFrame({"time": time, "visibility": visibility})
    communication_windows['start_of_streak'] = communication_windows.visibility.ne(communication_windows['visibility'].shift()) #we define the initial points of a communication window
    communication_windows['streak_id'] = communication_windows['start_of_streak'].cumsum()
    communication_windows['streak_counter'] = communication_windows.groupby('streak_id').cumcount() + 1
    communication_windows['streak_counter_seconds'] = (communication_windows.groupby('streak_id').cumcount() + 1) * simulation_step_epoch
    shadow_df["partial"] = False
    if shadow_df.shape[0] == 0:
        return shadow_df
    if shadow_df.loc[0, "start"] == epochs[0]:
        shadow_df.loc[0, "partial"] = True
    if shadow_df.loc[shadow_df.index[-1], "end"] == epochs[-1]:
        shadow_df.loc[shadow_df.index[-1], "partial"] = True
    return visibility, elevation, time, communication_windows