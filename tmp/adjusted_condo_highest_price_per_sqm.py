import pandas as pd

def load_data(file_path):
    """Load data from a CSV file."""
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        print(f"Failed to load data: {e}")
        return None

def clean_and_calculate_price_per_sqm(data):
    """Clean data and calculate price per sqm."""
    required_columns = ['rent_cd_price', 'rent_cd_floorarea', 'condo_name']
    if not all(col in data.columns for col in required_columns):
        print("Missing required columns for calculation.")
        return None
    
    data = data.dropna(subset=required_columns) 
    data = data[data['rent_cd_floorarea'] > 0] 
    
    data['price_per_sqm'] = data['rent_cd_price'] / data['rent_cd_floorarea']
    return data

def find_highest_price_per_sqm(data):
    """Find the condo with the highest price per sqm."""
    if 'price_per_sqm' not in data.columns:
        print("Price per sqm not calculated.")
        return None
    
    max_price_per_sqm_row = data.loc[data['price_per_sqm'].idxmax()]
    return max_price_per_sqm_row

def main():
    file_path = 'merge_ddprop_ggmap_unclean.csv'
    data = load_data(file_path)
    if data is not None:
        data = clean_and_calculate_price_per_sqm(data)
        if data is not None:
            result = find_highest_price_per_sqm(data)
            if result is not None:
                print(result)

if __name__ == "__main__":
    main()