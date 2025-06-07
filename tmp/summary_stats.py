import pandas as pd

def check_summary_stats(csv_file):
 df = pd.read_csv(csv_file)
 df['rent_cd_features_walk'] = pd.to_numeric(df['rent_cd_features_walk'], errors='coerce')
 summary_stats = df['rent_cd_features_walk'].describe()
 return summary_stats

csv_file = 'Data_Cleaned_AI.csv'
summary_stats = check_summary_stats(csv_file)
print(summary_stats)