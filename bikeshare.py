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
    # get user input for city (chicago, new york city, washington).
    valid=1
    while(valid):
        print('Which city\'s bikeshare data do you want to analyze?\n')
        print('Please choose a city from the following options:\n \tChicago\n \tNew York City\n \tWashington\n')
        city = input().lower()
        cities=['chicago','new york city','washington']
        if city in cities :
            valid=0
        else:
            print('Invalid option\n')
            if input('Would you like to try again?(Y/N)').lower() not in ['yes','y','ye','yeah']:
                valid=0
                return('','','')

    # get user input for month (all, january, february, ... , june)
    valid=1
    while(valid):
        print('Please enter a specific month from January to June to analyze or enter "all" for no month filter\n')
        month = input().lower()
        months = ['january','february','march','april','may','june','all']
        if month in months:
            valid=0
        else:
            print('Invalid option\n')
            if input('Would you like to try again?(Y/N)').lower() not in ['yes','y','ye','yeah']:
                valid=0
                return('','','')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    valid=1
    while(valid):
        print('Please enter a specific day from Monday to Sunday or enter "all" for no day filter\n')
        day = input().lower()
        days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all']
        if day in days:
            valid=0
        else:
            print('Invalid option\n')
            if input('Would you like to try again?(Y/N)').lower() not in ['yes','y','ye','yeah']:
                valid=0
                return('','','')

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
    df=pd.read_csv(CITY_DATA[city])
    #adding a column 'Month' to the date frame to help filter by month
    df['Month']=pd.DatetimeIndex(df['Start Time']).month
    #adding a column 'Day' to the date frame to help filter by day of the week
    df['Day']=pd.DatetimeIndex(df['Start Time']).weekday
    #adding a column 'hour' to the date frame to help filter by hour
    df['hour']=pd.DatetimeIndex(df['Start Time']).hour
    months_dict={'january':1,'february':2,'march':3,'april':4,'may':5,'june':6}
    days_dict={'monday':0,'tuesday':1,'wednesday':2,'thursday':3,'friday':4,'saturday':5,'sunday':6}
    if month in months_dict:
        df=df[df['Month']==months_dict[month]]
    if day in days_dict:
        df=df[df['Day']==days_dict[day]]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('-'*40)
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    mon=[]
    # display the most common month
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    popular_month = df['Month'].mode()[0]
    months_dict={1:'January',2:'February',3:'March',4:'April',5:'May',6:'June'}
    print("The peak month is",months_dict[popular_month],'\n')

    # display the most common day of week
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Day'] = df['Start Time'].dt.weekday
    popular_day = df['Day'].mode()[0]
    days_dict={0:'Monday',1:'Tuesday',2:'Wednesday',3:'Thursday',4:'Friday',5:'Saturday',6:'Sunday'}
    print("The peak day of the week is",days_dict[popular_day],'\n')

    # display the most common start hour
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print("The peak start hour is",popular_hour,'\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    input('Press enter to go back to main menu\n')


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('-'*40)
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    st_df = df.groupby( [ "Start Station"] ).size().reset_index()
    st_df.columns=["Start Station","Count"]
    max_count=st_df["Count"].idxmax()
    print("The most commonly used start station is",st_df["Start Station"][max_count])

    # display most commonly used end station
    en_df = df.groupby( [ "End Station"] ).size().reset_index()
    en_df.columns=["End Station","Count"]
    max_count=en_df["Count"].idxmax()
    print("The most commonly used end station is",en_df["End Station"][max_count])

    comb_df=df.groupby(["Start Station","End Station"]).size().reset_index()
    comb_df.columns=["Start Station","End Station","Count"]
    max_count=comb_df["Count"].idxmax()
    print("The most frequent combination of Start Station and End Station is",comb_df["Start Station"][max_count],"-",comb_df["End Station"][max_count])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    input('Press enter to go back to main menu\n')


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('-'*40)
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total travel time is {} seconds\n'.format(df['Trip Duration'].sum()))

    # display mean travel time
    print('Average travel time is {} seconds\n'.format(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    input('Press enter to go back to main menu\n')


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('-'*40)
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Counts for each user type\n',df.groupby(['User Type']).size(),'\n')

    # Display counts of gender
    if 'Gender' in df.columns:
        print('Counts for each gender\n',df.groupby(['Gender']).size())
    else:
        print('Gender data is missing\n')

    if 'Birth Year' in df.columns:
        # Display earliest, most recent, and most common year of birth
        print("\nThe earliest year of birth is",int(df["Birth Year"].min()))
        print("The most recent year of birth is",int(df["Birth Year"].max()))

        birth_df=df.groupby(["Birth Year"]).size().reset_index()
        birth_df.columns=["Birth Year","Count"]
        max_count=birth_df["Count"].idxmax()
        print("The most common year of birth is",int(birth_df["Birth Year"][max_count]))
    else:
        print("Birth year data is missing\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    input('Press enter to go back to main menu\n')

def display_raw_data(df):
    """ Displays the raw data from the selected city bikeshare data """
    print('-'*40)
    i=0
    j=5
    while True:
        print(df[i:j])
        check=input("Would you like to see another 5 rows of raw data?(Y/N)\n")
        if check.lower() not in ['yes','y','ye','yeah']:
            break
        elif df.shape[0]-j >= 5:
            i=j
            j=j+5
        elif df.shape[0]-j < 5:
            i=j
            j=df.shape[0]
            print(df[i:j])
            print("There is no more raw data to display\n")
            break
    input('Press enter to go back to main menu\n')

def main():
    while True:
        city, month, day = get_filters()
        if city=='' or month == '' or day == '':
            print("Thanks for trying out our analysis on bikeshare data!Have a great day!")
            break
        df = load_data(city, month, day)
        valid=1
        while(valid):
            print('Please choose the type of analysis you would like to see\n')
            print('\tFor Time Stats : enter 1\n')
            print('\tFor Station Stats : enter 2\n')
            print('\tFor Trip Duration Stats : enter 3\n')
            print('\tFor User Stats : enter 4\n')
            print('\tFor viewing raw data : enter 5\n')
            print('\tFor exiting current data analysis : enter 6\n')
            option=input()
            if option=='1':
                time_stats(df)
            elif option=='2':
                station_stats(df)
            elif option=='3':
                trip_duration_stats(df)
            elif option=='4':
                user_stats(df)
            elif option=='5':
                display_raw_data(df)
            elif option=='6':
                valid=0
            else:
                print('Invalid option')
                if input('Would you like to try again?(Y/N)').lower() not in ['yes','y','ye','yeah']:
                    valid=0
        restart = input('\nWould you like to restart?(Y/N)\n')
        if restart.lower() not in ['yes','y','ye','yeah']:
            print("Thanks for trying out our analysis on bikeshare data!Goodbye!")
            break


if __name__ == "__main__":
	main()
