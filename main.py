import pandas as pd
from distance_calculator import getDistanceBetweenPoints
import seaborn as sns
import datetime
import numpy as np


def main():
    # All dataframe info
    set_pandas_display_options()
    data = pd.read_csv('201701-citibike-tripdata.csv', sep=',', parse_dates=['Start Time', 'Stop Time'])
    print(data)
    print("-----------------------------------------------------------------------------------)")
    showDistanceForEachRide(data)
    getDistanceAccordingToGender(data)
    getTop5MostUsedStations(data)
    getTop5MostUsedBikes(data)



def getDistanceAccordingToGender(data):
    data['Gender'].where(~(data.Gender == 1), other="Man", inplace=True)
    data['Gender'].where(~(data.Gender == 2), other="Woman", inplace=True)
    data['Gender'].where(~(data.Gender == 0), other="Unknown gender", inplace=True)
    print(data.groupby(['Gender'])['Distance'].mean())


def showDistanceForEachRide(data):
    print("Distance for each ride")
    data['Distance'] = getDistanceBetweenPoints(
        data['Start Station Latitude'],
        data['Start Station Longitude'],
        data['End Station Latitude'],
        data['End Station Longitude']
    )
    data.update(data[['Distance']].fillna(0))
    print(data)


def getTop5MostUsedStations(data):
    print(
        data.groupby(['Start Station ID'])['Start Station ID'].count().reset_index(name='Number of visits').sort_values(
            ['Number of visits']).tail().iloc[::-1]
    )


def getTop5MostUsedBikes(data):
    print(
        data[['Trip Duration', 'Bike ID']].groupby(['Bike ID']).count().reset_index().sort_values(by=['Trip Duration']).tail().iloc[::-1]
    )


def dependenceOfDurationOfRideOnAgeAndGender(data):
    pass
def set_pandas_display_options() -> None:
    display = pd.options.display
    display.max_columns = 100
    display.max_rows = 100
    display.max_colwidth = 199
    display.width = None


if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
