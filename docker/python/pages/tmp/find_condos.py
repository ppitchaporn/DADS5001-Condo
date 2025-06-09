import pandas as pd

def find_condos_with_3_bedrooms(file_path):
    # Load the data
    data = pd.read_csv(file_path)
    
    # Filter the data for condos with 3 bedrooms
    condos_with_3_bedrooms = data[data['rent_cd_bed'] == 3]
    
    # Identify the locations of these condos
    locations = condos_with_3_bedrooms[['new_condo_name', 'rent_cd_features_station']]
    
    return locations

if __name__ == "__main__":
    file_path = "Data_Cleaned_AI.csv"
    locations = find_condos_with_3_bedrooms(file_path)
    print(locations)