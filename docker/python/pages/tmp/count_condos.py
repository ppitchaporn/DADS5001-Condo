import pandas as pd
def count_condos_with_3_or_more_bathrooms(condos_df):
    condos_with_3_or_more_bathrooms = condos_df[condos_df['bathrooms'] >= 3]
    return len(condos_with_3_or_more_bathrooms)
def main():
    data = {
        'condo_id': [1, 2, 3, 4, 5],
        'bathrooms': [2, 3, 1, 4, 3]
    }
    condos_df = pd.DataFrame(data)
    count = count_condos_with_3_or_more_bathrooms(condos_df)
    return count
if __name__ == "__main__":
    answer = main()
    print(answer)