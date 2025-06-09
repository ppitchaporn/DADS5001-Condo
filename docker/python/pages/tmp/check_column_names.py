import pandas as pd

def check_column_names(csv_file):
 # Read the CSV file
 df = pd.read_csv(csv_file)

 # Return the column names
 return df.columns.tolist()

if __name__ == "__main__":
 csv_file = "Data_Cleaned_AI.csv"
 column_names = check_column_names(csv_file)
 print(column_names)