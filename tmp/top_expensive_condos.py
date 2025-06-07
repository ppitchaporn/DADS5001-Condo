import pandas as pd
def get_top_expensive_condos(csv_file):
 # Read the CSV file into a pandas DataFrame with specified encoding
 df = pd.read_csv(csv_file, encoding='latin1')
 # Convert rent_cd_price to numeric values
 df['rent_cd_price'] = pd.to_numeric(df['rent_cd_price'].str.replace(',', ''), errors='coerce')
 # Sort the DataFrame by rent_cd_price in descending order
 df_sorted = df.sort_values(by='rent_cd_price', ascending=False)
 # Select the top10 rows from the sorted DataFrame
 top_10_condos = df_sorted.head(10)
 return top_10_condos
if __name__ == "__main__":
 csv_file = "merge_ddprop_ggmap_unclean.csv"
 top_10_condos = get_top_expensive_condos(csv_file)
 print(top_10_condos)