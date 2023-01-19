from datetime import timedelta, datetime
from typing import Dict

import numpy as np
from pyproj import Transformer
from tudatpy.kernel.astro import time_conversion
from tudatpy.kernel.astro.time_conversion import julian_day_to_calendar_date, seconds_since_epoch_to_julian_day
from useful_functions import get_input_data



def compute_visibility(pos_ecf, station, dates_name):
    """
    Compute the visibility of the spacecraft from a given ground station.
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
    return visibility, elevation, time