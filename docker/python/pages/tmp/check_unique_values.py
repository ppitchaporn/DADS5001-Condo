import pandas as pd

def check_unique_values(file_path):
    try:
        data = pd.read_csv(file_path, encoding='latin1')
        unique_condo_name = data['condo_name'].nunique()
        data['rent_cd_price'] = pd.to_numeric(data['rent_cd_price'], errors='coerce')
        data = data.dropna(subset=['rent_cd_price'])
        unique_rent_cd_price = data['rent_cd_price'].nunique()
        top_10 = data.nlargest(10, 'rent_cd_price')[['condo_name', 'rent_cd_price']]
        return top_10
    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == "__main__":
    file_path = "merge_ddprop_ggmap_unclean.csv"
    result = check_unique_values(file_path)
    print(result)