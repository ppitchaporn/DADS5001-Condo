import pandas as pd

def find_highest_priced_condo(csv_file):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)
    
    # Find the row with the maximum price
    max_price_row = df.loc[df['rent_cd_price'].idxmax()]
    
    # Get the condo name and price
    condo_name = max_price_row['new_condo_name']
    max_price = max_price_row['rent_cd_price']
    
    return condo_name, max_price

if __name__ == "__main__":
    csv_file = 'Data_Cleaned_AI.csv'
    condo_name, max_price = find_highest_priced_condo(csv_file)
    print(f"The condo with the highest price is {condo_name} with a price of {max_price} THB.")