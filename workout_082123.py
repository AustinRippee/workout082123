import pandas as pd
import math
import matplotlib.pyplot as plt

df = pd.read_csv("workout_082123.csv")

# Function to convert "m:ss" format to seconds as a float
def time_str_to_seconds(time_str):
    try:
        if ':' in time_str:
            minutes, seconds = time_str.split(':')
            total_seconds = int(minutes) * 60 + float(seconds)
            return total_seconds
        else:
            return 0  # Handle cases where time format is not valid
    except ValueError:
        return 0  # Handle invalid time format gracefully
    
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


# Clean and convert '2mi' column
df['2mi'] = df['2mi'].apply(lambda x: x if ':' in str(x) else '0:00')
df['2mi'] = df['2mi'].apply(time_str_to_seconds)

df['2mi_in_sec'] = df['2mi']
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

# Sort the DataFrame by '2mi' in ascending order and '800avg' in descending order
df = df.sort_values(by=['2mi', '800avg'], ascending=[True, True])

ax1 = df.plot.scatter(x='2mi', y='800avg', c='DarkBlue')

# Get the x and y limits of the plot
x_min, x_max = ax1.get_xlim()
y_min, y_max = ax1.get_ylim()

# Reverse the x-axis and y-axis limits to achieve the desired sorting
ax1.set_xlim(x_max, x_min)  # Reverse x-axis
ax1.set_ylim(y_max, y_min)  # Reverse y-axis

plt.show()

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