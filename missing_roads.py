import pandas as pd
import html5lib
import matplotlib.pyplot as plt
import numpy as np

#open the files
missing_road_list = pd.read_csv('Missing_roads', sep = '\t')
cleaned_roads = pd.read_csv('cleaned_all_road_data kopie.csv', sep = '\t')

#create dataframes
missing_road_list = list(missing_road_list.columns.unique())
missing_road = pd.DataFrame(missing_road_list, columns = ['Road'])
cleaned_roads_missing = pd.merge(missing_road, cleaned_roads, on='Road', how='inner')
#cleaned_roads_missing.Description = cleaned_roads_missing.Description.str.lower()

df_bridge = cleaned_roads_missing[cleaned_roads_missing.LRPType == 'Bridge']
df_culvert = cleaned_roads_missing[cleaned_roads_missing.LRPType == 'Culvert']
df_bridge_culvert = #append , then sort on road , sort on LRPNo!!

df_bridge[df_bridge.Description.str.contains('start') == True]
df_bridge[df_bridge.Description.str.contains('end') == True]


