import pandas as pd
import matplotlib
import seaborn as sns
import datetime as dt


matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

from distance_calculator import getDistanceBetweenPoints


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
    dependenceOfDurationOfRideOnAgeAndGender(data)
    do_men_and_women_prefer_different_directions(data)


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
        data[['Trip Duration', 'Bike ID']].groupby(['Bike ID']).count().reset_index().sort_values(
            by=['Trip Duration']).tail().iloc[::-1]
    )


def dependenceOfDurationOfRideOnAgeAndGender(data):
    data['Birth Year'] = data['Birth Year'].fillna(0).astype(int)
    current_year = dt.date.today().year
    data['Age'] = current_year - data['Birth Year']
    data['Age'].where(~(data['Age'] == 2022), other=0, inplace=True)

    grouped_data = data[['Trip Duration', 'Age', 'Gender']].groupby(['Age', 'Gender']).mean().reset_index()
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.set(title='The average value of the duration of the trip depending on age and gender')
    ill = sns.barplot(data=grouped_data, x=grouped_data['Age'], y=grouped_data['Trip Duration'],
                      hue=grouped_data['Gender'], width=1
                      , saturation=1, palette='rocket_r')
    plt.show()


def  do_men_and_women_prefer_different_directions(data):
    grouped_data = data[['End Station Latitude', 'End Station Longitude','Gender']].groupby(['Gender','End Station Latitude', 'End Station Longitude']).all().reset_index().drop([0])
    grouped_data = grouped_data.loc[grouped_data['Gender'] != 'Unknown gender']
    print(grouped_data)
    sns.set_color_codes()
    sns.scatterplot(data=grouped_data,x=grouped_data['End Station Latitude'],y=grouped_data['End Station Longitude'],hue=grouped_data['Gender'],palette=['b','r'],style=grouped_data['Gender'])
    plt.show()
def set_pandas_display_options() -> None:
    display = pd.options.display
    display.max_columns = 100
    display.max_rows = 100
    display.max_colwidth = 199
    display.width = None


if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
