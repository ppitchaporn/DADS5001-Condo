import pandas as pd

def main():
    try:
        df = pd.read_csv('Data_Cleaned_AI.csv')
        if 'new_condo_name' in df.columns:
            unique_condo_names = df['new_condo_name'].unique()
            for name in unique_condo_names:
                print(name)
        else:
            print("The 'new_condo_name' column does not exist in the CSV file.")
    except FileNotFoundError:
        print("The specified CSV file does not exist.")
    except pd.errors.EmptyDataError:
        print("The CSV file is empty.")
    except pd.errors.ParserError:
        print("Error parsing the CSV file.")

if __name__ == "__main__":
    main()