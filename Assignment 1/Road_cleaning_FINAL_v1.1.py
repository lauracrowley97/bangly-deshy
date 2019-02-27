#whaooooo
# import libraries
import pandas as pd
import html5lib
import matplotlib.pyplot as plt
import numpy as np

global df
global df_original
global diff_cutoff
global diff_cutoff_lat_dk
global counter 
global road_cleaned

counter = 0
diff_cutoff_lon = 0
diff_cutoff_lat = 0
df = pd.DataFrame()
df_original = pd.DataFrame()
road_cleaned = pd.DataFrame()

import_data()


def import_data():
     # doing all files together
     # read in htm file
     roadnames = pd.read_csv('roadnames.csv') # need to have roadnames list in same folder path 
     roadnames_list = list(roadnames.columns.unique())
     for roadname in roadnames_list:
          filename = "{}.lrps.htm".format(roadname)
          f =  open(filename, "rb")
          list_road = pd.read_html(f, skiprows = 2) # check skip rows
          df_road = list_road[-1] # check argument
          f.close()
          #original datafile
          global df
          df = df_road.iloc[:,1:7]
          df.columns = ["LRPNo","RoadChainage","LRPType","Description","LatitudeDec","LongitudeDec"]
          df["Road"] = roadname
          #df = '{} = pd.DataFrame'.format(roadname)
          #pd.to_numeric(df["LatitudeDec"], downcast="integer") #coerce as float
          #pd.to_numeric(df["LongitudeDec"], downcast="integer") #coerce as float
          global df_original
          df_original = df
          determine_outliers()
     road_cleaned.to_csv("cleaned_all_road_data.csv", sep='\t')
print('x')


def plot_road(x):   
     #plot the road with mistakes
     plt.plot(x.LongitudeDec, x.LatitudeDec)
     plt.title("Road")
     plt.xlabel("Longitude")
     plt.ylabel("Latitude")
     plt.show()
print("x")

##########COPIED CODE FROM WORKING EXAMPLE ##################################

def determine_outliers():
     #Get the differences between up and down
     global df
     global counter
     global diff_cutoff_lon
     global diff_cutoff_lat
     global road_cleaned
     if counter < 4: 
          counter = counter + 1
          #calculate the longitudeDec
          df_diff_lon1 = [abs(df.LongitudeDec - df.LongitudeDec.shift(-1)) for row in df.LongitudeDec]
          df_diff_lon2 = [abs(df.LongitudeDec - df.LongitudeDec.shift(1)) for row in df.LongitudeDec]
          df["Difference_down_lon"] = df_diff_lon1[0]
          df["Difference_up_lon"] = df_diff_lon2[0]
          
          #calculate the LatitudeDec
          df_diff_lat1 = [abs(df.LatitudeDec - df.LatitudeDec.shift(-1)) for row in df.LatitudeDec]
          df_diff_lat2 = [abs(df.LatitudeDec - df.LatitudeDec.shift(1)) for row in df.LatitudeDec]
          df["Difference_down_lat"] = df_diff_lat1[0]
          df["Difference_up_lat"] = df_diff_lat2[0]
          
          #determine the std and cut-off value
          diff_lon_std = df.Difference_up_lon.std()
          diff_lat_std = df.Difference_up_lat.std()
          diff_cutoff_lon = (4*diff_lon_std)
          diff_cutoff_lat = (4*diff_lat_std)
          
          #find outliers based on calculated differences between points
          find_replace_outliers()
     else:
          counter = 0
          plot_road(df)
          road_cleaned = road_cleaned.append(df)

print("x")


def find_replace_outliers():
    #select the outliers in a different dataframe
     global df
     outliers = pd.DataFrame()
     outliers1 = df.loc[df["Difference_up_lon"] > diff_cutoff_lon  ]
     outliers2 = df.loc[df["Difference_down_lon"] > diff_cutoff_lon  ]
     outliers3 = df.loc[df["Difference_up_lat"] > diff_cutoff_lat ]
     outliers4 = df.loc[df["Difference_down_lat"] > diff_cutoff_lat ]


     outliers = outliers.append(outliers1)
     outliers = outliers.append(outliers2)
     outliers = outliers.append(outliers3)
     outliers = outliers.append(outliers4)
     
     outliers = outliers.drop_duplicates().sort_values(by=['LRPNo'])
     outliers['middle_outlier_lon'] = np.where((outliers['Difference_up_lon'] > diff_cutoff_lon) & (outliers['Difference_down_lon'] > diff_cutoff_lon ), True,False)
     outliers['middle_outlier_lat'] = np.where((outliers['Difference_up_lat'] > diff_cutoff_lat) & (outliers['Difference_down_lat'] > diff_cutoff_lat ), True,False)
     
     #average out the wrong values for the LongitudeDec
     indeces_list_lon = outliers.index[outliers['middle_outlier_lon'] == True].tolist()
     indeces_list_lat = outliers.index[outliers['middle_outlier_lat'] == True].tolist()

     outliers["replaced"] = ""

     for i in indeces_list_lon:
          k = i + 1
          m = i - 1
          average_longitudeDec = ( outliers.LongitudeDec[k] + outliers.LongitudeDec[m] ) / 2 
          outliers.LongitudeDec[i] = average_longitudeDec
          outliers.replaced[i] = True

     for i in indeces_list_lat:
          g = i + 1
          f = i - 1
          average_latitudeDec = ( outliers.LatitudeDec[g] + outliers.LatitudeDec[f] ) / 2 
          outliers.LatitudeDec[i] = average_latitudeDec
          outliers.replaced[i] = True

     indeces_list = []
     indeces_list = indeces_list_lat + indeces_list_lon
     to_be_merged_rows = outliers.loc[outliers["replaced"] == True]
     to_be_merged_rows = to_be_merged_rows.drop(["Difference_up_lat","Difference_up_lon" ,"Difference_down_lat","Difference_down_lon","middle_outlier_lat","middle_outlier_lon"],axis =1)
     
     df = df.drop(["Difference_down_lat", "Difference_up_lat", "Difference_up_lon", "Difference_down_lon"], axis =1)
     df = df.drop(indeces_list)
     df = df.append(to_be_merged_rows)     
     df = df.sort_index()
     determine_outliers()

print('x')


df = road_cleaned.loc[road_cleaned["Road"] == "N1"].sort_index()
plot_road(df)
del df
del road_cleaned

find_grouped_outliers()

road_names_list_n1n4 = ["N4","N1"]

dk = pd.DataFrame()
del df

def find_grouped_outliers():
     #Get the differences between up and down
     global dk
     global road_cleaned

     for i in road_names_list_n1n4:
        dk = road_cleaned.loc[road_cleaned["Road"]==i]
        dk["replaced_grouped"] = ""
        print(dk)
        #find_grouped_lat_outliers()

print('x')

find_grouped_outliers()
find_grouped_lat_outliers_find_indeces()
find_grouped_lat_outliers_change_them()


find_grouped_lat_outliers()

indeces_list_lat = []


road_cleaned
def find_grouped_lat_outliers_find_indeces():
    global dk
    global diff_cutoff_lat_dk
    global indeces_list_lat
    dk["Difference_down_lat"] = [abs(dk.LatitudeDec - dk.LatitudeDec.shift(-1)) for row in dk.LatitudeDec]
    dk_difference_lat = [abs(dk.LatitudeDec - dk.LatitudeDec.shift(-1)) for row in dk.LatitudeDec]
    dk["Difference_down_lat"] = dk_difference_lat[0]
    
    diff_lat_std_dk = dk.Difference_down_lat.std()
    diff_cutoff_lat_dk = (5*diff_lat_std_dk)
    indeces_list_lat = dk.index[dk['Difference_down_lat'] > diff_cutoff_lat].tolist()
    print(indeces_list_lat)
print('z')



dk["LatitudeDec"][765:800]
indeces_list_lat


def find_grouped_lat_outliers_change_them():
    global dk
    for i in indeces_list_lat:
        k = i + 1
        dk.LatitudeDec[k] = dk.LatitudeDec[i] + diff_cutoff_lat_dk
        dk.replaced_grouped[k] = True
print('x')


def drop_zeros():
    #def filter_zeros():
    # #Load in cleaned dataframe
    road_cleaned = pd.read_csv("cleaned_all_road_data_output.csv", sep = "\t")
    #select datapoints in certain scope 
    road_cleaned["zero_lon"] = np.where(road_cleaned["LongitudeDec"] < 10,True, False )
    road_cleaned["zero_lat"] = np.where(road_cleaned["LatitudeDec"] < 10,True, False )
    
    #drop the faulty points
    road_cleaned.drop(road_cleaned.loc[road_cleaned['zero_lon']==False].index, inplace=True)
    road_cleaned.drop(road_cleaned.loc[road_cleaned['zero_lat']==False].index, inplace=True)

print('x')
