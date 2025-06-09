import math
import pandas as pd

def calculate_distance(lat1, lon1, lat2, lon2):
    # Radius of the earth in km
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = R * c
    return d

def find_closest_bts(condo, bts_stations):
    closest_bts = None
    min_distance = float('inf')
    for index, bts in bts_stations.iterrows():
        distance = calculate_distance(condo['latitude'], condo['longitude'], bts['latitude'], bts['longitude'])
        if distance < min_distance:
            min_distance = distance
            closest_bts = bts['name']
    return closest_bts, min_distance

def main():
    # Sample data for condos and BTS stations
    condos_data = {
        'name': ['Condo A', 'Condo B', 'Condo C'],
        'latitude': [13.7563, 13.7443, 13.7363],
        'longitude': [100.5018, 100.5138, 100.5238]
    }
    
    bts_stations_data = {
        'name': ['BTS A', 'BTS B', 'BTS C'],
        'latitude': [13.7583, 13.7453, 13.7383],
        'longitude': [100.5038, 100.5128, 100.5258]
    }
    
    condos = pd.DataFrame(condos_data)
    bts_stations = pd.DataFrame(bts_stations_data)
    
    closest_condo = None
    min_distance = float('inf')
    
    for index, condo in condos.iterrows():
        _, distance = find_closest_bts(condo, bts_stations)
        if distance < min_distance:
            min_distance = distance
            closest_condo = condo['name']
    
    print(f"The condo closest to a BTS station is {closest_condo} with a distance of {min_distance} km.")

if __name__ == "__main__":
    main()