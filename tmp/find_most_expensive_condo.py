import pandas as pd

def find_most_expensive_condo(csv_file):
    try:
        data = pd.read_csv(csv_file)
    except FileNotFoundError:
        return "File not found."
    except pd.errors.EmptyDataError:
        return "No data in the file."
    except pd.errors.ParserError:
        return "Error parsing the file."

    required_columns = ['new_condo_name', 'rent_cd_price']
    if not all(column in data.columns for column in required_columns):
        return "The file is missing required columns."

    max_price_row = data.loc[data['rent_cd_price'].idxmax()]

    return max_price_row['new_condo_name']

if __name__ == "__main__":
    csv_file = "Data_Cleaned_AI.csv"
    most_expensive_condo = find_most_expensive_condo(csv_file)
    print(most_expensive_condo)