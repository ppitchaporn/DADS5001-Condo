import pandas as pd

def calculate_highest_price_per_sqm(csv_file):
 # Read the CSV file into a DataFrame with specified encoding
 df = pd.read_csv(csv_file, encoding='latin1')

 # Ensure the necessary columns are of the correct type
 df['rent_cd_price'] = pd.to_numeric(df['rent_cd_price'], errors='coerce')
 df['rent_cd_floorarea'] = pd.to_numeric(df['rent_cd_floorarea'], errors='coerce')

 # Calculate price per sqm
 df['price_per_sqm'] = df['rent_cd_price'] / df['rent_cd_floorarea']

 # Identify the condo with the highest price per sqm
 max_price_per_sqm_condo = df.loc[df['price_per_sqm'].idxmax()]

 return max_price_per_sqm_condo

def main():
 csv_file = 'merge_ddprop_ggmap_unclean.csv'
 result = calculate_highest_price_per_sqm(csv_file)
 print(result)

if __name__ == "__main__":
 main()