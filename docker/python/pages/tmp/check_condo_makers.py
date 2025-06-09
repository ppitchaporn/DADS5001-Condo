import pandas as pd
def check_condo_makers_data(file_path):
    try:
        data = pd.read_csv(file_path)
        condo_maker_columns = [col for col in data.columns if 'maker' in col.lower() or 'developer' in col.lower()]
        if condo_maker_columns:
            return condo_maker_columns
        else:
            return "No columns related to condo makers found."
    except Exception as e:
        return f"An error occurred: {e}"
if __name__ == "__main__":
    file_path = "Data_Cleaned_AI.csv"
    result = check_condo_makers_data(file_path)
    print(result)