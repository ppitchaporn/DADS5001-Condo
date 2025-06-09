import pandas as pd

def analyze_data(csv_file):
 df = pd.read_csv(csv_file, encoding='latin1')
 print("Data Shape:", df.shape)
 print("Columns:", df.columns)
 print("Missing Values Count:\n", df.isnull().sum())
 print("Summary Statistics:\n", df.describe())

def main():
 csv_file = 'merge_ddprop_ggmap_unclean.csv'
 analyze_data(csv_file)

if __name__ == "__main__":
 main()