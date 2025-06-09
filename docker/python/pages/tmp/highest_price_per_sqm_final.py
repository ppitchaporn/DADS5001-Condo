import pandas as pd

def calculate_highest_price_per_sqm(csv_file):
    df = pd.read_csv(csv_file, encoding='latin1')
    df['rent_cd_price'] = pd.to_numeric(df['rent_cd_price'], errors='coerce')
    df['rent_cd_floorarea'] = pd.to_numeric(df['rent_cd_floorarea'], errors='coerce')
    df_filtered = df[(df['rent_cd_price'].notna()) & (df['rent_cd_floorarea'] > 0)]
    if df_filtered.empty:
        return "No valid data found for calculation."
    df_filtered['price_per_sqm'] = df_filtered['rent_cd_price'] / df_filtered['rent_cd_floorarea']
    max_price_per_sqm_condo = df_filtered.loc[df_filtered['price_per_sqm'].idxmax()]
    return max_price_per_sqm_condo

def main():
    csv_file = 'merge_ddprop_ggmap_unclean.csv'
    result = calculate_highest_price_per_sqm(csv_file)
    return result

if __name__ == "__main__":
    result = main()
    print(result)