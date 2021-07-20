import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTHS_LIST = ['January', 'February', 'March', 'April', 'May', 'June'] 
DAYS_LIST = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'] 

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    # Declare initial value for month and day to handle if user not select one of them or both for filter
    month, day = '', ''
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Would you like to see data for for Chicago, New York City, or Washington?\n')
        validate_city = validate_input('city', city)
        if validate_city:
            print(validate_city)
        else:
            break
    
    while True:
        # get user input for filter (month, day, both, or none)
        filters = input(f'Would you like to filter the data by month, day, both, or not at all? '
                          f'type "none" for no time filter.\n')

        validate_filters = validate_input('filters', filters)
        if validate_filters:
            print(validate_filters)
        else:
            break
    
    filters = filters.lower()
    if filters != 'none':
        # get user input for month (all, january, february, ... , june)
        filters = filters.lower()
        if filters in ['both', 'month']:
            while True:
                month = input(f'Which month? January, February, Mrach, April, May, June, or All? '
                              f'Please type out the full month name.\n')

                validate_month = validate_input('month', month)
                if validate_month:
                    print(validate_month)
                else:
                    month = month.upper()
                    break
        # get user input for day of week (all, monday, tuesday, ... sunday)
        if filters in ['both', 'day']:
            while True:
                day = input(f'Which day? Monday, Tuesday, Wednesday, Thursday, '
                            f'Friday, Saturday, or All? Please type out the full day name.\n')

                validate_day = validate_input('day', day)

                if validate_day:
                    print(validate_day)
                else:
                    break

    print('-'*40)
    return city, month, day

def validate_input(input_name:str, input_value:any) -> str:
    """
    Validate the input user entered for a city, month, and day to analyze.
    
    Args:
        (str) input_name - name of the input to analyze
        (str) input_value - value of the input to analyze
    Returns:
        (str) input_validate - the result of validation
    """
    input_validate = ''
    MONTHS = MONTHS_LIST + ['All']
    DAYS = DAYS_LIST + ['All']
    if not isinstance(input_value, str) or not input_value.strip() or input_value.isdigit():
        input_validate = f'Warrning --> Please enter the {input_name} as it mentioned in the Question.\n'
    
    elif input_name == 'city' and input_value.title().strip() not in ['Chicago', 'New York City', 'Washington']:
        input_validate = f'Please enter the {input_name} as it mentioned in the Question.\n'
    
    elif input_name == 'filters' and input_value.lower().strip() not in ['both', 'day', 'month', 'none']:
        input_validate = f'Please enter the {input_name} as it mentioned in the Question.\n'
    
    elif input_name == 'month' and input_value.title().strip() not in MONTHS:
        input_validate = f'Please enter the {input_name} as it mentioned in the Question.\n'
    
    elif input_name == 'day' and input_value.title().strip() not in DAYS:
        input_validate = f'Please enter the {input_name} as it mentioned in the Question.\n'
    return input_validate
    
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
    df = pd.read_csv(CITY_DATA[city.lower()])
    month = month.title()
    day = day.title()
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
#     df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['day_of_week'] = df['Start Time'].dt.day_name()
    
    # filter by month if applicable
    if month not in ['', 'All']:
        # use the index of the months list to get the corresponding int
        month = MONTHS_LIST.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
    
    # filter by day of week if applicable
    if day not in ['', 'All']:
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month from the Start Time column to create an month column
    df['month'] = df['Start Time'].dt.month
    
    # extract week from the Start Time column to create an week column
    df['week'] = df['Start Time'].dt.week
    
    
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    
    # display the most common month
    popular_month = df['month'].mode()[0]
    print('Most Popular Start Month::\n', popular_month)
    
    # display the most common day of week
    popular_week = df['week'].mode()[0]
    print('Most Popular Start Week::\n', popular_week)
    
    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour::\n', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most Popular Start Station::\n', popular_start_station)
    
    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most Popular End Station::\n', popular_end_station)

    # display most frequent combination of start station and end station trip
    popular_start_end_station = df[['Start Station', 'End Station']].mode().loc[0]
    print('Most Popular End Station::\n', popular_start_end_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total Travel Time is::\n', total_travel_time)
    # display mean travel time
    average_travel_time = df['Trip Duration'].mean()
    print('Average of Travel Time is::\n', average_travel_time)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Count of the User Type is ::\n', user_types)
    
    # Display counts of gender
    if 'Gender' in df.columns:
        gender = df['Gender'].value_counts()
        print('Count of the Gender is ::\n', gender)

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        most_common_year_of_birth = df['Birth Year'].mode()[0]
        print('Most common year of birth is ::\n', most_common_year_of_birth)
        
        earliest_year_of_birth = df['Birth Year'].min()
        print('Earliest year of birth is ::\n', earliest_year_of_birth)
        
        most_recent_year_of_birth = df['Birth Year'].max()
        print('Most of recent year of birth is ::\n', most_recent_year_of_birth)
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """Displays 5 rows of individual trip data."""
    
    start_loc = 0
    view_first_5_rows_of_data = ''
    while True:
        view_first_5_rows_of_data = input('\nDo you want to see the first 5 rows of data? Enter yes or no\n').lower().strip()
        if view_first_5_rows_of_data not in ['yes','no']:
            print('Please enter only one of these answer yes or no')
        else:
            print(df.iloc[start_loc:start_loc + 5])
            break
    if view_first_5_rows_of_data == 'yes':
        while True:
            view_next_5_rows_of_data = input('\nDo you want to see the next 5 rows of data? Enter yes or no\n').lower()
            if view_next_5_rows_of_data.strip() == 'yes':
                start_loc += 5
                print(df.iloc[start_loc:start_loc + 5])
            else:
                if view_next_5_rows_of_data not in ['yes','no']:
                    print('Please enter only one of these answer yes or no')
                else:
                    break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()