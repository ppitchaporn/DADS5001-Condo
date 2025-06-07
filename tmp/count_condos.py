import pandas as pd
def count_condos_with_3_or_more_bathrooms(csv_file):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file)
    # Filter the DataFrame to include rows where 'rent_cd_bath' is 3 or more
    filtered_df = df[df['rent_cd_bath'] >= 3]
    # Count the number of rows in the filtered DataFrame
    count = len(filtered_df)
    return count
if __name__ == "__main__":
    csv_file = "Data_Cleaned_AI.csv"
    result = count_condos_with_3_or_more_bathrooms(csv_file)
    print(result)