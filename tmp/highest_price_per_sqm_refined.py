import pandas as pd

def calculate_highest_price_per_sqm(csv_file):
    # Read the CSV file into a DataFrame with specified encoding
    df = pd.read_csv(csv_file, encoding='latin1')

    # Ensure the necessary columns are of the correct type and not missing
    df['rent_cd_price'] = pd.to_numeric(df['rent_cd_price'], errors='coerce')
    df['rent_cd_floorarea'] = pd.to_numeric(df['rent_cd_floorarea'], errors='coerce')

    # Filter out rows where either price or floor area is missing or zero
    df_filtered = df[(df['rent_cd_price'].notna()) & (df['rent_cd_floorarea'] > 0)]

    # Calculate price per sqm
    df_filtered['price_per_sqm'] = df_filtered['rent_cd_price'] / df_filtered['rent_cd_floorarea']

    # Identify the condo with the highest price per sqm
    if not df_filtered.empty:
        max_price_per_sqm_condo = df_filtered.loc[df_filtered['price_per_sqm'].idxmax()]
        return max_price_per_sqm_condo
    else:
        return "No valid data found for calculation."

def main():
    csv_file = 'merge_ddprop_ggmap_unclean.csv'
    result = calculate_highest_price_per_sqm(csv_file)
    print(result)

if __name__ == "__main__":
    main()