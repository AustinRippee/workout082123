import pandas as pd
import math

df = pd.read_csv("workout_082123.csv")

# Function to convert "m:ss" format to seconds as a float
def time_str_to_seconds(time_str):
    try:
        if ':' in time_str:
            minutes, seconds = time_str.split(':')
            total_seconds = int(minutes) * 60 + float(seconds)
            return total_seconds
        else:
            return None  # Handle cases where time format is not valid
    except ValueError:
        return None  # Handle invalid time format gracefully
    
def seconds_to_time_str(total_seconds):
    if math.isnan(total_seconds):
        return None
    minutes = int(total_seconds // 60)
    seconds = int(total_seconds % 60)
    return f"{minutes}:{seconds:02d}"

# Custom conversion function to convert to float or return None for 'X'
def convert_to_float_or_none(value):
    try:
        if value == 'X':
            return None
        return float(value)
    except ValueError:
        return None

df['2mi_in_sec'] = df['2mi'].apply(time_str_to_seconds)
df['800.1_in_sec'] = df['800'].apply(time_str_to_seconds)
df['800.2_in_sec'] = df['800.1'].apply(time_str_to_seconds)
df['800.3_in_sec'] = df['800.2'].apply(time_str_to_seconds)
df['400'] = df['400'].apply(convert_to_float_or_none)

df['800avg'] = df[['800.1_in_sec', '800.2_in_sec', '800.3_in_sec']].mean(axis=1)
df['8toMi'] = df[['800avg']] * 2
df['4to2'] = df['400'] / 2.0
df['3miEst'] = df['2mi_in_sec'] + df['8toMi']
df['5kEst'] = df['2mi_in_sec'] + df['8toMi'] + df['4to2']

df['8toMi'] = df['8toMi'].apply(seconds_to_time_str)
df['800avg'] = df['800avg'].apply(seconds_to_time_str)
df['3miEst'] = df['3miEst'].apply(seconds_to_time_str)
df['5kEst'] = df['5kEst'].apply(seconds_to_time_str)

#df1 = df[['Name', '2mi']].sort_values(['2mi'], ascending=True)

#print(df)
#print()
#print(df[['Name', '8toMi']])
#print()
#print(df[['Name', '800avg']].sort_values(['800avg'], ascending=True))
#print()
#print(df[['Name', '5kEst']].sort_values(['5kEst'], ascending=True))

# Display the DataFrame
#print(df[['Name', '2mi', '800avg']])