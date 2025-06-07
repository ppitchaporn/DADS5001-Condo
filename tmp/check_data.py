import pandas as pd

def check_data(file_path):
    try:
        data = pd.read_csv(file_path, encoding='latin1')
        if 'rent_cd_price' not in data.columns or 'condo_name' not in data.columns:
            return "Either 'rent_cd_price' or 'condo_name' column is missing."
        missing_condo_name = data['condo_name'].isnull().sum()
        missing_rent_cd_price = data['rent_cd_price'].isnull().sum()
        return f"Missing 'condo_name': {missing_condo_name}, Missing 'rent_cd_price': {missing_rent_cd_price}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == "__main__":
    file_path = "merge_ddprop_ggmap_unclean.csv"
    result = check_data(file_path)
    print(result)