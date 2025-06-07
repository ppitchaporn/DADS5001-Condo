import pandas as pd
def find_condos_with_3_bedrooms(file_path):
    # Read the CSV file
    data = pd.read_csv(file_path)
    
    # Filter condos with 3 bedrooms
    condos_with_3_bedrooms = data[data['rent_cd_bed'] == 3]
    
    return condos_with_3_bedrooms

if __name__ == "__main__":
    file_path = "Data_Cleaned_AI.csv"
    condos_with_3_bedrooms = find_condos_with_3_bedrooms(file_path)
    print(condos_with_3_bedrooms)