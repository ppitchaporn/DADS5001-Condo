import pandas as pd

def calculate_total_price(csv_file):
    try:
        # Read the CSV file
        df = pd.read_csv(csv_file)
        
        # Check if 'rent_cd_price' column exists
        if 'rent_cd_price' in df.columns:
            # Calculate the total price
            total_price = df['rent_cd_price'].sum()
            return total_price
        else:
            return "Error: 'rent_cd_price' column not found in the CSV file."
    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == "__main__":
    csv_file = "Data_Cleaned_AI.csv"
    total_price = calculate_total_price(csv_file)
    print(total_price)