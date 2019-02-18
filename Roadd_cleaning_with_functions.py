#whaooooo
# import libraries
import pandas as pd
import html5lib
import matplotlib.pyplot as plt
import numpy as np

#def find_outliers():
#     import_data()
#     determine_outliers(df)     

def import_data():
# read in htm file
    f =  open("N4.lrps.htm", "rb")
    list_road = pd.read_html(f, skiprows = 4)
    df_road = list_road[2] #ask rob to update this, when the argument is 1 it duplicates the data!
#original datafile
    global df
    df = df_road.iloc[:,1:7]
    df.columns = ["LRPNo","RoadChainage","LRPType","Description","LatitudeDec","LongitudeDec"]
    pd.to_numeric(df["LatitudeDec"], downcast="integer") #coerce as float
    pd.to_numeric(df["LongitudeDec"], downcast="integer") #coerce as float
    global df_original
    df_original = df
#plot original road for visual inspection
    plot_road(df_original)
print('x')

import_data()


def plot_road(x):   
     #plot the road with mistakes
     plt.plot(x.LongitudeDec, x.LatitudeDec)
     plt.title("Road")
     plt.xlabel("Longitude")
     plt.ylabel("Latitude")
     plt.show()

print('x')

determine_outliers(df)

def determine_outliers(x):
    #Get the differences between up and down
     df_diff_lon1 = [abs(x.LongitudeDec - x.LongitudeDec.shift(-1)) for row in x.LongitudeDec]
     df_diff_lon2 = [abs(x.LongitudeDec - x.LongitudeDec.shift(1)) for row in x.LongitudeDec]
     x["Difference_down"] = df_diff_lon1[0]
     x["Difference_up"] = df_diff_lon2[0]
    #determine the std and cut-off value
     diff_lon_std = x.Difference_up.std()
     global diff_cutoff
     diff_cutoff = (4*diff_lon_std)

     if diff_cutoff > 0.001:
          find_replace_outliers(df,df_original, diff_cutoff)
     else:
          print("no futher outliers, go to next file")

print("x")


find_replace_outliers(df,df_original,0.005)

def find_replace_outliers(x,p,diff_cutoff):
    #select the outliers in a different dataframe
     outliers = pd.DataFrame()
     outliers1 = x.loc[x["Difference_up"] > diff_cutoff  ]
     outliers2 = x.loc[x["Difference_down"] > diff_cutoff  ]
     outliers = outliers.append(outliers1)
     outliers = outliers.append(outliers2)
     outliers = outliers.drop_duplicates().sort_values(by=['LRPNo'])
     outliers['middle_outlier'] = np.where((outliers['Difference_up'] > diff_cutoff) & (outliers['Difference_down'] > diff_cutoff), True,False)
    #average out the wrong values for the LongitudeDec
     indeces_list = outliers.index[outliers['middle_outlier'] == True].tolist()
     outliers["replaced"] = ""

     for i in indeces_list:
          k = i + 1
          m = i - 1
          average_longitudeDec = ( outliers.LongitudeDec[k] + outliers.LongitudeDec[m] ) / 2 
          outliers.LongitudeDec[i] = average_longitudeDec
          outliers.replaced[i] = True

     to_be_merged_rows = outliers.loc[outliers["replaced"] == True]
     to_be_merged_rows = to_be_merged_rows.drop(["Difference_up", "Difference_down","middle_outlier"],axis =1)

     df_original = p.drop(indeces_list)
     df_original = df_original.append(to_be_merged_rows)
     df_original = df_original.sort_values(by=['LRPNo'])
     plot_road(df_original)
     determine_outliers(df_original)

print('x')