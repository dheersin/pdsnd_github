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
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    valid_city = False
    while not valid_city:
        city = input('What city would you like to learn about (Chicago, New York, or Washington D.C.)? ')
        if city.lower() in ['chicago', 'new york city', 'washington']:
            valid_city = True
        else:
            print('That is not a valid choice. Please check your spelling and try again.\n')

    # TO DO: get user input for month (all, january, february, ... , june)
    valid_month = False
    while not valid_month:
        month = input('What month would you like to learn about? Valid options are january-june or all.')
        if month.lower() in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
            valid_month = True
        else:
            print('That is not a valid choice. Please check your spelling and try again.\n')

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    valid_day = False
    while not valid_day:
        day = input('What day would you like to learn about? Valid options are sunday-saturday or all.')
        if day.lower() in ['all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']:
            valid_day = True
        else:
            print('That is not a valid choice. Please check your spelling and try again.\n')

    print('-'*40)
    return city.lower(), month.lower(), day.lower()


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
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract hour, month, and day of week from Start Time to create new columns
    df['hour'] = df['Start Time'].dt.hour
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

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
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df['month'].mode()[0]

    print('Most Popular Rental Month: {}'.format(popular_month))

    # TO DO: display the most common day of week
    popular_day = df['day_of_week'].mode()[0]

    print('Most Popular Rental Day of the Week: {}'.format(popular_day))

    # TO DO: display the most common start hour
    popular_hour = df['hour'].mode()[0]

    print('Most Popular Rental Starting Hour: {}'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]

    print('Most Popular Starting Location: {}'.format(popular_start_station))

    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]

    print('Most Popular Ending Location: {}'.format(popular_end_station))

    # TO DO: display most frequent combination of start station and end station trip
    popular_trip_start_station, popular_trip_end_station = df.groupby(['Start Station', 'End Station']).size().idxmax()

    print('Most Popular Route: Start at {} and end at {}.'.format(popular_trip_start_station, popular_trip_end_station))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_time = df['Trip Duration'].sum()
    total_years = total_time // (60*60*24*365)
    total_days = (total_time - (total_years * 60*60*24*365)) // (60*60*24)
    total_mins = (total_time - (total_years * 60*60*24*365) - (total_days * 60*60*24)) // (60*60)
    total_secs = (total_time - (total_years * 60*60*24*365) - (total_days * 60*60*24) - (total_mins * 60*60)) // 60
    
    print('Total travel time is: {} seconds. This is {} year(s), {} day(s), {} minute(s), and {} second(s)'.format(total_time, total_years, total_days, total_mins, total_secs))


    # TO DO: display mean travel time
    mean_time = df['Trip Duration'].mean() 
    mean_mins = mean_time // 60
    mean_secs = mean_time % 60

    print('Mean travel time is: {} seconds. This is {} minute(s) and {} second(s)'.format(mean_time, mean_mins, mean_secs))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()

    print('Here is a breakdown of users by type: \n')
    print(user_types)

    # TO DO: Display counts of gender
    if city != 'washington':
        genders = df['Gender'].value_counts()

        print('Here is a breakdown of users by gender: \n')
        print(genders)

    # TO DO: Display earliest, most recent, and most common year of birth
        oldest = min(df['Birth Year'])
        youngest = max(df['Birth Year'])
        most_common = df['Birth Year'].mode()[0]
    
        print('\nThe oldest user was born in {}.'.format(oldest))
        print('\nThe youngest user was born in {}.'.format(youngest))
        print('\nThe most common birth year is {}.'.format(most_common))
    else:
        print('There is no gender or birth year data for Washington D.C.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        
        ask_again = True
        start_pos = 0
        while ask_again:
            raw_data = input('\nWould you like to see the raw data? Enter yes or no.\n')    
            if raw_data.lower() == 'yes':
                print(df.iloc[np.arange(start_pos, start_pos + 5)])
                start_pos += 5
                continue_data = input('\nWould you like to continue? Enter yes or no.\n')
                if continue_data.lower() != 'yes':
                    ask_again = False
            else:
                break
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
