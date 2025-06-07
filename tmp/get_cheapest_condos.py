import pandas as pd

def get_cheapest_condos_in_jatujak(csv_file):
 try:
 data = pd.read_csv(csv_file, encoding='latin1')
 except Exception as e:
 print(f"Error reading CSV: {e}")
 return None

 jatujak_condos = data[data['Location'].str.contains('¨µØ¨Ñ¡Ã', case=False, na=False)]
 cheapest_condos = jatujak_condos.nsmallest(5, 'Price')
 return cheapest_condos[['Project Name', 'Price']]

if __name__ == "__main__":
 csv_file = 'Data_Cleaned_AI.csv'
 cheapest_condos = get_cheapest_condos_in_jatujak(csv_file)
 if cheapest_condos is not None:
 print(cheapest_condos)