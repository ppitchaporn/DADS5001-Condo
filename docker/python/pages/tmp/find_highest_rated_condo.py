import pandas as pd

def find_highest_rated_condo(csv_file):
    try:
        condo_ratings = pd.read_csv(csv_file)
        required_columns = ['Condo Name', 'Review Star Rating']
        if not all(column in condo_ratings.columns for column in required_columns):
            return "The CSV file is missing required columns."
        highest_rated_condo = condo_ratings.loc[condo_ratings['Review Star Rating'].idxmax()]
        return highest_rated_condo['Condo Name']
    except FileNotFoundError:
        return "The specified CSV file was not found."
    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == "__main__":
    csv_file = 'condo_ratings.csv'
    result = find_highest_rated_condo(csv_file)
    print(result)