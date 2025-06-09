import pandas as pd

def find_closest_condo_to_bts(csv_file):
 # Load the dataset
 df = pd.read_csv(csv_file)
 
 # Ensure 'near_rail_meter' is numeric
 df['near_rail_meter'] = pd.to_numeric(df['near_rail_meter'], errors='coerce')
 
 # Filter out rows where 'near_rail_meter' is NaN
 df_filtered = df.dropna(subset=['near_rail_meter'])
 
 # Find the minimum distance
 min_distance = df_filtered['near_rail_meter'].min()
 
 # Identify the condo(s) with the minimum distance
 closest_condos = df_filtered[df_filtered['near_rail_meter'] == min_distance]
 
 return closest_condos[['new_condo_name', 'near_rail_meter']]

# Run the function
csv_file = 'Data_Cleaned_AI.csv'
closest_condos = find_closest_condo_to_bts(csv_file)
print(closest_condos)