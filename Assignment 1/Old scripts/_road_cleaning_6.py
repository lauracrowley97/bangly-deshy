#whaooooo
# import libraries
import pandas as pd
import html5lib
import matplotlib.pyplot as plt
import numpy as np

<<<<<<< HEAD
def find_outliers():
     import_data()
     determine_outliers(df)     
=======
# read in htm file
f =  open("N4.lrps.htm", "rb")
list_road = pd.read_html(f, skiprows = 4)
df_road = list_road[2] #ask rob to update this, when the argument is 1 it duplicates the data!
df = df_road.iloc[:,1:7]
df.columns = ["LRPNo","RoadChainage","LRPType","Description","LatitudeDec","LongitudeDec"]
pd.to_numeric(df["LatitudeDec"], downcast="integer") #coerce as float
pd.to_numeric(df["LongitudeDec"], downcast="integer") #coerce as float

#plot the road with mistakes
plt.plot(df.LongitudeDec, df.LatitudeDec)
plt.title("Road")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.show()

#Get the Mean and Standard Dev from the Lon and Lat
LonMean = df.LongitudeDec.mean()
LatMean = df.LatitudeDec.mean()
LonStd = df.LongitudeDec.std()
LatStd = df.LatitudeDec.std()

#df['LonPlus1'] = df.LongitudeDec.shift(1)
#df['LonMin1'] = df.LongitudeDec.shift(-1)
#df.head()

# below commented out to be replaced by next section (with list comprehension)
#df[abs(df.LongitudeDec - df.LongitudeDec.shift(-1)) > LonStd]
#df[abs(df.LongitudeDec - df.LongitudeDec.shift(1)) > LonStd]

#list comprehension
#[ expression for item in list if conditional ]
#df_outliers = [(abs(row - row.shift(-1)) > LonStd) for row in df.LongitudeDec]
#take distance betwen point and point after it
#take std dev o those distances
#make range of distances between points thats acceptable
#check distance between point and point after it against range, marking where it's too large

df_diff_lon = [abs(df.LongitudeDec - df.LongitudeDec.shift(-1)) for row in df.LongitudeDec]
df["Difference"] = df_diff_lon[0]
diff_lon_mean = df.Difference.mean()
diff_lon_std = df.Difference.std()
diff_cutoff = (2.698*diff_lon_std)

#df_diff_lon = [abs(df.LongitudeDec - df.LongitudeDec.shift(-1)) for row in df.LongitudeDec]
#df_diff_lon = df_diff_lon[0]
#diff_lon_mean = df_diff_lon.mean()
#diff_lon_std = df_diff_lon.std()

#df_diff_lon = pd.DataFrame(df_diff_lon)
#df_diff_lon.plot.box(sym='r+')
#plt.show()

#outliers = [df["Outlier"].istrue() for row in df if (df.Difference > diff_cutoff)]

outliers = pd.DataFrame()
for i in range(len(df1.LongitudeDec))
for row in df:
    print(type(row))
    break 


    #if (df.Difference[row] > diff_cutoff):
     #   outliers.append(df.iloc[row+1])
    #else:
     #   continue
        

df_outliers = [(abs(df.LongitudeDec - df.LongitudeDec.shift(-1)) > LonStd) for row in df.LongitudeDec]
df_outliers = pd.DataFrame(df_outliers)
df_outliers.to_csv("/Users/castanos/Documents/06 Graduate TU Delft/2018 Q3 Discrete/outliers.csv", sep='\t')

>>>>>>> 363c7224a0a16ea32280b0e656b8bd0daf10241f

def import_data():
# read in htm file
     f =  open("N4.lrps.htm", "rb")
     list_road = pd.read_html(f, skiprows = 4)
     df_road = list_road[2] #ask rob to update this, when the argument is 1 it duplicates the data!
#original datafile
     df = df_road.iloc[:,1:7]
     df.columns = ["LRPNo","RoadChainage","LRPType","Description","LatitudeDec","LongitudeDec"]
     pd.to_numeric(df["LatitudeDec"], downcast="integer") #coerce as float
     pd.to_numeric(df["LongitudeDec"], downcast="integer") #coerce as float
     global df_original = df
#plot original road for visual inspection
     plot_road(df_original)


def plot_road(x):   
     #plot the road with mistakes
     plt.plot(x.LongitudeDec, x.LatitudeDec)
     plt.title("Road")
     plt.xlabel("Longitude")
     plt.ylabel("Latitude")
     plt.show()

def determine_outliers(x):
#Get the differences between up and down
     df_diff_lon1 = [abs(x.LongitudeDec - x.LongitudeDec.shift(-1)) for row in x.LongitudeDec]
     df_diff_lon2 = [abs(x.LongitudeDec - x.LongitudeDec.shift(1)) for row in x.LongitudeDec]
     x["Difference_down"] = df_diff_lon1[0]
     x["Difference_up"] = df_diff_lon2[0]

#determine the std and cut-off value
     diff_lon_std = x.Difference_up.std()
     diff_cutoff = (2.698*diff_lon_std)

     if diff_cutoff > 0.01:
          find_replace_outliers(df,df_original,diff_cutoff)
     else:
          print("no futher outliers, go to next file")

print("x")

determine_outliers(df)

df_original

find_replace_outliers(df,df_original,0.00050)

def find_replace_outliers(x,p,diff_cutoff):
#select the outliers in a different dataframe
     outliers = pd.DataFrame()
     outliers1 = x.loc[x["Difference_up"] > diff_cutoff  ]
     outliers2 = x.loc[x["Difference_down"] > diff_cutoff  ]
     outliers = outliers.append(outliers1)
     outliers = outliers.append(outliers2)
     outliers = outliers.drop_duplicates().sort_values(by=['LRPNo'])
     outliers['middle_outlier'] = np.where((outliers['Difference_up'] > diff_cutoff) & (outliers['Difference_down'] > diff_cutoff)
                     , True,False)

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
     to_be_merged_rows = to_be_merged_rows.drop(["Difference_up", "Difference_down","middle_outlier","replaced"],axis =1)

     df_original = p.drop(indeces_list)
     df_original = df_original.append(to_be_merged_rows)
     df_original = df_original.sort_values(by=['LRPNo'])
     df = df_original

     plot_road(df_original)
     determine_outliers(df)

print('x')

plot_road(df_original)
