"""
Program Name: bikeshare_2.py
Purpose:      Python script which explores US bikeshare data
"""
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ''
    while city != 'chicago' and city != 'new york city' and city != 'washington':
        city = input("Enter a city name (chicago, new york city, washington): ").lower()

    # get user input for month (all, january, february, ... , june)
    month = ''
    while month != 'january' and month != 'february' and month != 'march' and month != 'april' and month != 'may' and month != 'june' and month != 'all':
        month = input("Enter a month name (january, february, march, april, may, june, or all): ").lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ''
    while day != 'monday' and day != 'tuesday' and day != 'wednesday' and day != 'thursday' and day != 'friday' and day != 'saturday' and day != 'sunday' and day != 'all':
        day = input("Enter a day of the week (monday, tuesday, wednesday, thurday, friday, saturday, sunday, or all): ").lower()

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # specify filename using city name
    filename = city.replace(' ', '_')+'.csv'
    #print(filename)

    # load data file into a dataframe
    df = pd.read_csv(filename)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week & hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    # start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('Most Popular Month:', popular_month)

    # display the most common day of week
    popular_day_of_week = df['day_of_week'].mode()[0]
    print('Most Popular Day of Week:', popular_day_of_week)

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)

    # print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    # start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most Popular Start Station:', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most Popular End Station:', popular_end_station)

    # display most frequent combination of start station and end station trip, by creating a new column which combines those two aforementioned columns
    df['station_combination'] = df['Start Station'] + ' to ' + df['End Station']
    popular_station_combination = df['station_combination'].mode()[0]
    print('Most Popular Station Combination:', popular_station_combination)

    # print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    # start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    # print the seconds in a rounded format
    print('Total Travel Time (in seconds):', round(total_travel_time))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    # print the seconds in a rounded format
    print('Mean Travel Time (in seconds):', round(mean_travel_time))

    # print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    # start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Counts of User Types:\n', user_types)

    # Display counts of gender, if that data is available
    try: 
        genders = df['Gender'].value_counts()
        print('\nCounts of Gender:\n', genders)
    except Exception:
        print('\nSorry, no gender data available.')

    # Display earliest, most recent, and most common year of birth - if that data is available
    try: 
        # filter out anyone who is over 100 years old, as these might be data entry errors
        earliest_birth_year = df.loc[df['Birth Year'] > 1916, 'Birth Year'].min()
        latest_birth_year = df.loc[df['Birth Year'] > 1916, 'Birth Year'].max()
        popular_birth_year = df.loc[df['Birth Year'] > 1916, 'Birth Year'].mode()[0]
        # print the years in the integer format
        print('\nEarliest birth year:', int(earliest_birth_year))
        print('\nMost Recent birth year:', int(latest_birth_year))
        print('\nMost Common birth year:', int(popular_birth_year))
    except Exception:
        print('\nSorry, no birth year data available.')

    # print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        # execute function to get user-provided filtering criteria
        city, month, day = get_filters()
        # execute function to load data into a data frame, based on filter criteria
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # get user input to ascertain if they would like to view raw data
        view_counter = 0
        view_data = input('\nWould you like to view the raw data records? Enter yes or no.\n')
        while view_data.lower() == 'yes':
            # retrieve the next 5 records, and only show the columns from the raw data, ignoring the 4 new columns created by this program
            print(df.iloc[view_counter:view_counter+5,0:-4])
            # increment the counter by 5, and get user input again
            view_counter += 5
            view_data = input('\nWould you like to view the next 5 data records? Enter yes or no.\n')

        # get user input to ascertain if they'd like to start again or finish up
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
