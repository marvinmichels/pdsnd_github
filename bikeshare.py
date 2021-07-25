import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_user_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!\n')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = '' #An empty variable to save the user input of the city selection

    while city.lower() not in ['chicago','new york city','nyc','new york','washington']: #This loop repeats until the user input is correct
        city = input('For which city do you want to analyze the data?\n'
                    'Please type in Chicago, New York City or Washington: ')
        if city.lower() == 'chicago':
            print('\nWoohoo, you have choosen Chicago!\n')
        elif city.lower() == 'new york city' or city.lower() == 'nyc' or city.lower() == 'new york':
            print('\nNew York City is your choice!\n')
            city = "new york city"
        elif city.lower() == 'washington':
            print('\nNice, you have choosen the Capitol city Washington!\n')
        else:
            print('\nWrong input. Please choose between "Chicago", "New York City" and "Washington".\n')
    city = city.lower() #Saves the input in lower cases


    # get user input for month (all, january, february, ... , june)
    month = '' #An empty variable to save the user input of the time period (month) selection

    while month.lower() not in ['all','january','february','march','april','may','june']: #This loop repeats until the user input is correct
        month = input('For which time period do you want to evaluate the data?\n'
                      'Please type in "All" or "January", "February" and so on until "June": ')
        if month.lower() == 'all':
            print('\nYou want to look at the entire period.\n')
        #I wanted to avoid "elif", but still didn't let the line run too long. Therefore I split the month into two different groups. 
        elif month.lower() == 'january' or month.lower() == 'february' or month.lower() == 'march': 
            print('\nYou just want to look at the {} data.\n'.format(month.title()))
        elif month.lower() == 'april' or month.lower() == 'may' or month.lower() == 'june':
            print('\nYou just want to look at the {} data.\n'.format(month.title()))
        else:
            print('\nWrong input. Please choose between "All" or one of the month "January" to "June".\n')
    month = month.lower() #Saves the input in lower cases


    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = '' #An empty variable to save the user input of the day selection

    while day.lower() not in ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']: #This loop repeats until the user input is correct
        day = input('Do you want to evaluate data for a whole week or just for a specific day?\n'
                    'Please type in "All" or "Monday", "Tuesday" and so on until "Sunday": ')
        if day.lower() == 'all':
            print('\nYou would like to have a look at the entire week.\n')
        elif day.lower() == 'monday' or day.lower() == 'tuesday' or day.lower() == 'wednesday' or day.lower() == 'thursday':
            print('\nYou just want to look at the {} data.\n'.format(day.title()))
        elif day.lower() == 'friday' or day.lower() == 'saturday' or day.lower() == 'sunday':
            print('\nYou just want to look at the {} data.\n'.format(day.title()))
        else:
            print('\nWrong input. Please choose between "All" or a day from "Monday" to "Sunday".\n')
    day = day.lower() #Saves the input in lower cases


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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    #Combine Start and End Station to find most common Trip
    df['start_to_end_station'] = df['Start Station'] + " to " + df['End Station']

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


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # display the most common month
    if month == 'all':
        # extract month from the Start Time column to create an month column
        df['month'] = df['Start Time'].dt.month
        # find the most common month
        most_common_month = df['month'].mode()[0]
        months = {1: "January", 2: "February", 3: "March", 4: "April", 5:"May", 6:"June"}
        month_in_letters = months[most_common_month] #Searches for the key (month number) in the dictionary "months" and returns the value. In that case, the month written out.
        print('The most common month is: {} ({})'.format(month_in_letters, most_common_month))
    else:
        #If only one month (not "all") is selected, there is no most common month. So this message helps the user.
        print('The most common month is: You have choosen {}. So there is only this month within the filtered data.'.format(month.title()))

    # display the most common day of week
    if day == 'all':
        # extract day of week from the Start Time column to create an day of week column
        df['day_of_week'] = df['Start Time'].dt.weekday_name
        # find the most common day of week
        most_common_dayofweek = df['day_of_week'].mode()[0]
        print('The most common day of week is:', most_common_dayofweek)
    else:
        #If only one day (not "all") is selected, there is no most common day of week. So this message helps the user.
        print('The most common day of week is: You have choosen {}. So there is only this day within the filtered data.'.format(day.title()))

    # display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    # find the most popular hour
    popular_hour = df['hour'].mode()[0]
    print('The most popular start hour is:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print('The most common Start Station is:', most_common_start_station)

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print('The most common End Station is:', most_common_end_station)

    # display most frequent combination of start station and end station trip
    most_frequent_connection = df['start_to_end_station'].mode()[0] #Looks at the new column "start_to_end_station" and checks which value occurs most frequently.
    print('The most frequent connection is:', most_frequent_connection)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('The total travel time in seconds is:', total_travel_time)
    #The values in the database show the travel time in seconds. To make it easier for the user, the program converts it into minutes and hours.
    total_travel_time = total_travel_time/60
    print('The total travel time in minutes is:', total_travel_time)
    total_travel_time = total_travel_time/60
    print('The total travel time in hours is:', total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('The mean travel time in seconds is:', mean_travel_time)
    #The values in the database show the travel time in seconds. To make it easier for the user, the program converts it into minutes and hours.
    mean_travel_time = mean_travel_time/60
    print('The mean travel time in minutes is:', mean_travel_time)
    mean_travel_time = mean_travel_time/60
    print('The mean travel time in hours is:', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #Display counts of user types
    print('The following information shows the distribution of the individual user types:\n')
    print(df['User Type'].value_counts())
    print('\n')

    # Display counts of gender
    if 'Gender' in df.columns: #Checks whether there is a "Gender" column in the data frame. For example, the Washington data set does not have such a column.
        print('The following information shows the distribution of the user genders:\n')
        print(df['Gender'].value_counts())
    else:
        print('There a no gender information for {}.\n'.format(city.title()))

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns: #Checks whether there is a "Birth Year" column in the data frame. For example, the Washington data set does not have such a column.
        print('\n')
        earliest_birth_year = int(df['Birth Year'].min())
        print('The earliest birth year is:', earliest_birth_year)
        most_recent_birth_year = int(df['Birth Year'].max())
        print('The most recent birth year is:', most_recent_birth_year)
        most_common_birth_year = int(df['Birth Year'].mode()[0])
        print('The most common birth year is:', most_common_birth_year)
    else:
        print('There a no birth year information for {}.\n'.format(city.title()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_user_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        
        #The following variables are used to show the raw data to the user. 
        show_raw_data = ''
        show_more_raw_data = ''
        rows_in_dataset = len(df.index)
        i = 5

        while show_raw_data.lower() not in ['y','n']:
            show_raw_data = input('Would you like to see five rows of raw data? Enter "Y" for yes and "N" for no: ')
            print('\n')
            if show_raw_data.lower() == 'y':
                print(df.iloc[:i])
                print('\n')
                while show_more_raw_data.lower() != 'n':
                    show_more_raw_data = input('Would you like to see five more rows? Enter "Y" for yes and "N" for no: ')
                    print('\n')
                    if show_more_raw_data.lower() == 'y':
                        if i <= rows_in_dataset - 5:
                            i = i+5
                            print(df.iloc[i-5:i])
                            print('\n')
                    elif show_more_raw_data.lower() == 'n':
                        continue
                    else:
                        print('Wrong input. Please choose bewtween "Y" for Yes or "N" for No.')
            elif show_raw_data.lower() == 'n':
                continue
            else:
                print('Wrong input. Please choose bewtween "Y" for Yes or "N" for No.')
            
        restart = input('\nWould you like to restart the program? Enter "Y" for yes and "N" for no: ')
        if restart.lower() != 'y':
            break


if __name__ == "__main__":
	main()
