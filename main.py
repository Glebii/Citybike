import pandas as pd
from distance_calculator import getDistanceBetweenPoints
import seaborn as sns
import datetime
import numpy as np


def main():
    # All dataframe info with debug
    set_pandas_display_options()
    data = pd.read_csv('201701-citibike-tripdata.csv', sep=',', parse_dates=['Start Time', 'Stop Time'])
    print(data)
    print("-----------------------------------------------------------------------------------)")
    showDistanceForEachRide(data)


def showDistanceForEachRide(data):
    data['Distance'] = getDistanceBetweenPoints(
        data['Start Station Latitude'],
        data['Start Station Longitude'],
        data['End Station Latitude'],
        data['End Station Longitude']
    )
    print(data)


def set_pandas_display_options() -> None:
    display = pd.options.display
    display.max_columns = 100
    display.max_rows = 100
    display.max_colwidth = 199
    display.width = None


if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
