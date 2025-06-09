import pandas as pd

def load_data(file_name):
    try:
        data = pd.read_csv(file_name)
        return data
    except Exception as e:
        print(f"Failed to load data: {e}")
        return None

def find_most_expensive_condo(data):
    if data is not None:
        if 'price' in data.columns:
            data['price'] = pd.to_numeric(data['price'], errors='coerce')
            most_expensive_condo = data.loc[data['price'].idxmax()]
            return most_expensive_condo
        else:
            print("Data is missing 'price' column.")
    return None

def main():
    file_name = 'condo_prices.csv'
    data = load_data(file_name)
    most_expensive_condo = find_most_expensive_condo(data)
    if most_expensive_condo is not None:
        print(most_expensive_condo)

if __name__ == "__main__":
    main()