import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import rasterio
from rasterio.plot import show
from matplotlib.colors import ListedColormap

car_assignments_merged_data_mod = pd.read_csv('car-assignments.csv')
cc_data_merged_data_mod = pd.read_csv('cc_data.csv')
gps_data_merged_data_mod = pd.read_csv('gps.csv')
loyalty_data_merged_data_mod = pd.read_csv('loyalty_data.csv')
gps_data = pd.read_csv('gps.csv')
merged_data = pd.merge(car_assignments_merged_data_mod, cc_data_merged_data_mod, on=['FirstName', 'LastName'])
merged_data_mod = merged_data[merged_data['CarID'].isin([31.0])]
# print(merged_data_mod.head(10))
gps_data_mod = gps_data.loc[gps_data['id'] == 106]
print(gps_data_mod.head(10))

tif_file = 'MC2-tourist_modified.tif'
with rasterio.open(tif_file) as src:
    tif_array = src.read(1)  # read first band of the TIFF image
gps_data_mod['Timestamp'] = pd.to_datetime(gps_data_mod['Timestamp'])
grouped_gps_data = gps_data_mod.groupby(gps_data_mod['Timestamp'].dt.date)
cmap = ListedColormap(sns.color_palette("viridis", len(grouped_gps_data)))

for date, group in grouped_gps_data:
    plt.figure(figsize=(10, 8))
    plt.imshow(tif_array, cmap='gray', extent=rasterio.plot.plotting_extent(src))
    points = plt.scatter(group['long'], group['lat'], c=group['Timestamp'].dt.hour, cmap='viridis', s=50, alpha=0.7)
    plt.colorbar(label='Hour of Day', ticks=np.arange(0, 24, 2))
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title(f'Path of CarID 106 (Truck)z on TIFF Map - Day {date}')
    plt.grid(True)
    plt.tight_layout()
    plt.show()
