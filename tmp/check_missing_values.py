import pandas as pd

def check_missing_values(csv_file):
 df = pd.read_csv(csv_file)
 missing_values_count = df['rent_cd_features_walk'].isnull().sum()
 return missing_values_count

csv_file = 'Data_Cleaned_AI.csv'
missing_values_count = check_missing_values(csv_file)
print(missing_values_count)