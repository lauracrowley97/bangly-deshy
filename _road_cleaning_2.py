#whaooooo
# import libraries
import pandas as pd
import html5lib
import matplotlib.pyplot as plt

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

# Make row by row comparison
df_compare = df.iloc[218:221,:]
df_compare_lat_mean = df_compare.LatitudeDec.mean()
df_compare_lat_std = df_compare.LatitudeDec.std()
df_compare_lon_mean = df_compare.LongitudeDec.mean()
df_compare_lon_std = df_compare.LongitudeDec.std()
df_outliers = df_compare[df_compare['LongitudeDec'] > (df_compare_lon_mean + df_compare_lon_std)]
df_outliers = df_outliers.append(df_compare[df_compare['LongitudeDec'] < (df_compare_lon_mean - df_compare_lon_std)])# = df_compare[df_compare['LongitudeDec'] < (df_compare_lon_mean - df_compare_lon_std)]

