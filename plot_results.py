import matplotlib.pyplot as plt
import pandas as pd

# 0: Paul, 1: Alfons
current_user = 1
if current_user == 0:
    current_path = 'etc'
elif current_user == 1:
    current_path = 'C:/Users/ARF/Code/arosty/tu_berlin/'
    
current_path += 'alg-eng/history/'
    
# PUT IN THE TIMESTAMPS OF THE FILES THAT YOU WANT TO COMPARE:
timestamps = ['201910311157', '201910311239']
# CHOOSE THE COLORS FOR THE PLOTTER:
colors = ['red', 'green']

pd.set_option('display.max_columns', None)

data = []

for stamp in timestamps:
    current_file = current_path + stamp + '_run_history.csv'
    new_df = pd.read_csv(current_file)
    new_df.time_in_seconds = new_df.time_in_seconds.str.rstrip('s')
    numeric_columns = [1,2,3,4]
    for col in numeric_columns:
        new_df[new_df.columns[col]] = pd.to_numeric(new_df[new_df.columns[col]])
    data.append(new_df)

# data.plot(kind='scatter', x=data.index, y='time_in_seconds')

for idx, df in enumerate(data):
    plt.scatter(df.index, df.time_in_seconds, color=colors[idx])
plt.ylabel('Time in seconds')
plt.show()
