import pandas as pd

# Simulating data fetch from a database or API
def fetch_condo_data():
 # Hypothetical data for demonstration
 data = {
 "Condo Name": ["Condo A", "Condo B", "Condo C"],
 "Price (THB)": [10000000,20000000,30000000]
 }
 return pd.DataFrame(data)

# Analyze the data to find the most expensive condo
def find_most_expensive_condo(df):
 most_expensive_condo = df.loc[df["Price (THB)"].idxmax()]
 return most_expensive_condo

# Main function
def main():
 condo_data = fetch_condo_data()
 most_expensive = find_most_expensive_condo(condo_data)
 return most_expensive

if __name__ == "__main__":
 result = main()
 print(result)