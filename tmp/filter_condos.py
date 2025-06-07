import pandas as pd
import re

def load_data(file_path):
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        print(f"Failed to load data: {e}")
        return None

def extract_walking_time(time_str):
    if pd.isnull(time_str):
        return None
    try:
        numbers = re.findall(r'\d+', str(time_str))
        if numbers:
            return int(numbers[0])
        else:
            return None
    except Exception as e:
        print(f"Error extracting walking time: {e}")
        return None

def filter_condos(data, max_distance=500):
    data['walking_time'] = data['rent_cd_features_walk'].apply(extract_walking_time)
    filtered_data = data[data['walking_time'] <= 7]
    return filtered_data

def main():
    file_path = 'Data_Cleaned_AI.csv'
    data = load_data(file_path)
    if data is not None:
        filtered_condos = filter_condos(data)
        print(filtered_condos[['new_condo_name', 'rent_cd_features_walk']])

if __name__ == "__main__":
    main()