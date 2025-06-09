import pandas as pd

def impute_missing_values_and_find_closest_condo(csv_file):
 # Load the dataset
 df = pd.read_csv(csv_file)
 
 # Ensure 'rent_cd_features_walk' is numeric
 df['rent_cd_features_walk'] = pd.to_numeric(df['rent_cd_features_walk'], errors='coerce')
 
 # Impute missing 'rent_cd_features_walk' with median
 median_walking_time = df['rent_cd_features_walk'].median()
 df['rent_cd_features_walk'] = df['rent_cd_features_walk'].fillna(median_walking_time)
 
 # Find the minimum walking time
 min_walking_time = df['rent_cd_features_walk'].min()
 
 # Identify the condo(s) with the minimum walking time
 closest_condos = df[df['rent_cd_features_walk'] == min_walking_time]
 
 return closest_condos[['new_condo_name', 'rent_cd_features_walk', 'rent_cd_features_station']]

# Run the function
csv_file = 'Data_Cleaned_AI.csv'
closest_condos = impute_missing_values_and_find_closest_condo(csv_file)
print(closest_condos)