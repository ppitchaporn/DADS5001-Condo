import pandas as pd

def load_data(file_path):
    """Load data from a CSV file."""
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        print(f"Failed to load data: {e}")
        return None

def calculate_price_per_sqm(data):
    """Calculate price per sqm."""
    # Ensure the necessary columns exist
    required_columns = ['rent_cd_price', 'rent_cd_floorarea']
    if not all(col in data.columns for col in required_columns):
        print("Missing required columns for calculation.")
        return None
    
    # Perform the calculation, avoiding division by zero
    data['price_per_sqm'] = data['rent_cd_price'] / data['rent_cd_floorarea']
    return data

def find_highest_price_per_sqm(data):
    """Find the condo with the highest price per sqm."""
    if 'price_per_sqm' not in data.columns:
        print("Price per sqm not calculated.")
        return None
    
    # Find the row with the maximum price per sqm
    max_price_per_sqm_row = data.loc[data['price_per_sqm'].idxmax()]
    return max_price_per_sqm_row

def main():
    file_path = 'merge_ddprop_ggmap_unclean.csv'
    data = load_data(file_path)
    if data is not None:
        data = calculate_price_per_sqm(data)
        if data is not None:
            result = find_highest_price_per_sqm(data)
            if result is not None:
                print(result)

if __name__ == "__main__":
    main()