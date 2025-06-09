import pandas as pd

def count_project_listings(csv_file):
 df = pd.read_csv(csv_file)
 project_counts = df['project_name'].value_counts()
 most_listed_project = project_counts.idxmax()
 count = project_counts.max()
 return most_listed_project, count

def main():
 csv_file = 'Data_Cleaned_AI.csv'
 most_listed_project, count = count_project_listings(csv_file)
 print(f"The project with the most listings is '{most_listed_project}' with {count} listings.")

if __name__ == "__main__":
 main()