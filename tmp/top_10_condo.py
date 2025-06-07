import pandas as pd

def get_top_10_most_expensive_condo(file_path):
    try:
        data = pd.read_csv(file_path, encoding='latin1')
        data['rent_cd_price'] = pd.to_numeric(data['rent_cd_price'], errors='coerce')
        data = data.dropna(subset=['rent_cd_price'])
        top_10 = data.nlargest(10, 'rent_cd_price')[['condo_name', 'rent_cd_price']]
        return top_10
    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == "__main__":
    file_path = "merge_ddprop_ggmap_unclean.csv"
    top_10_condo = get_top_10_most_expensive_condo(file_path)
    print(top_10_condo)