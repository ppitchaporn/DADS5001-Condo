import pandas as pd

def get_top_5_cheapest_condos(csv_file):
 # Read the CSV file
 df = pd.read_csv(csv_file)

 # Sort the data by price
 df_sorted = df.sort_values(by='rent_cd_price')

 # Extract the top 5 cheapest condos
 top_5_cheapest = df_sorted.head(5)

 return top_5_cheapest

if __name__ == "__main__":
 csv_file = "Data_Cleaned_AI.csv"
 top_5_cheapest = get_top_5_cheapest_condos(csv_file)
 print(top_5_cheapest)