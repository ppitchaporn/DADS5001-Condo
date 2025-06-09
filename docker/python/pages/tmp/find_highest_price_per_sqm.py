import pandas as pd

def find_highest_price_per_sqm(csv_file):
    # Read the CSV file
    df = pd.read_csv(csv_file)
    # Check if required columns exist
    if 'rent_cd_price' in df.columns and 'area_sqm' in df.columns:
        # Calculate price per sqm
        df['price_per_sqm'] = df['rent_cd_price'] / df['area_sqm']
        # Find the row with the highest price per sqm
        max_price_per_sqm_row = df.loc[df['price_per_sqm'].idxmax()]
        return max_price_per_sqm_row
    else:
        return "Required columns not found"

if __name__ == "__main__":
    csv_file = "Data_Cleaned_AI.csv"
    result = find_highest_price_per_sqm(csv_file)
    print(result)