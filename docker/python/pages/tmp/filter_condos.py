import pandas as pd

def filter_condos(condos_df):
    filtered_condos = condos_df[condos_df['num_reviews'] >= 100]
    return filtered_condos

def main():
    data = {
        'condo_name': ['Condo A', 'Condo B', 'Condo C', 'Condo D'],
        'num_reviews': [50, 120, 90, 150]
    }
    condos_df = pd.DataFrame(data)
    filtered_condos = filter_condos(condos_df)
    print(filtered_condos)

if __name__ == "__main__":
    main()