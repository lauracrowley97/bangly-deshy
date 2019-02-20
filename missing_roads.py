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
missing_bridge_culvert = cleaned_roads_missing[(cleaned_roads_missing.LRPType == 'Bridge') | (cleaned_roads_missing.LRPType == 'Culvert')]
missing_bridge_culvert = missing_bridge_culvert.drop(missing_bridge_culvert[missing_bridge_culvert.Description.str.contains('end|End|END') == True].index)
missing_bridge_culvert['Length'] = 'NaN'
missing_bridge_culvert.drop('replaced', axis = 1)
missing_bridge_culvert.to_csv("missing_bridge_culvert.csv", sep='\t')

