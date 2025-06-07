import pandas as pd

def find_most_expensive_condo(csv_file):
    # Read the CSV file
    df = pd.read_csv(csv_file)
    
    # Find the row with the maximum 'rent_cd_price'
    most_expensive_row = df.loc[df['rent_cd_price'].idxmax()]
    
    # Get the condo name
    most_expensive_condo = most_expensive_row['new_condo_name']
    most_expensive_price = most_expensive_row['rent_cd_price']
    
    return most_expensive_condo, most_expensive_price

if __name__ == "__main__":
    csv_file = "Data_Cleaned_AI.csv"
    condo_name, price = find_most_expensive_condo(csv_file)
    print(f"The most expensive condo is {condo_name} with a price of {price} THB.")