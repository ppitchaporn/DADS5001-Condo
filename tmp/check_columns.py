import pandas as pd

def check_columns(csv_file):
 df = pd.read_csv(csv_file)
 return list(df.columns)

csv_file = 'Data_Cleaned_AI.csv'
columns = check_columns(csv_file)
print(columns)