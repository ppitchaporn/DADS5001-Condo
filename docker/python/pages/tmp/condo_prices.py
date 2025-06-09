import pandas as pd

def get_condo_data():
    data = {
        'Condo Name': ['Condo A', 'Condo B', 'Condo C'],
        'Price': [10000000, 20000000, 15000000]
    }
    return pd.DataFrame(data)

def find_most_expensive_condo(df):
    most_expensive_condo = df.loc[df['Price'].idxmax()]
    return most_expensive_condo

def main():
    condo_df = get_condo_data()
    most_expensive = find_most_expensive_condo(condo_df)
    print(most_expensive)

if __name__ == "__main__":
    main()