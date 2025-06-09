import pandas as pd

def count_listings(csv_file):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(csv_file)
    
    # Count the number of listings for each condo project
    listing_counts = df['new_condo_name'].value_counts()
    
    # Identify the condo project with the most listings
    most_listings_project = listing_counts.idxmax()
    count = listing_counts.max()
    
    return most_listings_project, count

def main():
    csv_file = 'Data_Cleaned_AI.csv'
    most_listings_project, count = count_listings(csv_file)
    print(f"The condo project with the most listings is '{most_listings_project}' with {count} listings.")

if __name__ == "__main__":
    main()