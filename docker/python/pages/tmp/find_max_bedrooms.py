import pandas as pd
def find_condo_with_most_bedrooms(csv_file_path):
    df = pd.read_csv(csv_file_path)
    if not df.empty:
        max_bedrooms_row = df.loc[df['rent_cd_bed'].idxmax()]
        return max_bedrooms_row
    else:
        return "The DataFrame is empty."
csv_file_path = "Data_Cleaned_AI.csv"
result = find_condo_with_most_bedrooms(csv_file_path)
print(result)