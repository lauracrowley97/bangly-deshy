#whaooooo
# import libraries
import pandas as pd
import html5lib
import matplotlib.pyplot as plt

# read in htm file
f =  open("N4.lrps.htm", "rb")
list_road = pd.read_html(f, skiprows = 4)
df_road = list_road[2]
df = df_road.iloc[:,1:7]
df.columns = ["LRPNo","RoadChainage","LRPType","Description","LatitudeDec","LongitudeDec"]
#pd.to_numeric(df["LatitudeDec"], downcast="integer") #coerce as float
#pd.to_numeric(df["LongitudeDec"], downcast="integer") #coerce as float

#plot the road with mistakes
plt.plot(df.LongitudeDec, df.LatitudeDec)
plt.title("Road")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.show()

#create new columns with difference with the one below and above
df['below_Lon'] = abs(df.LongitudeDec - df.LongitudeDec.shift(-1))
df['above_Lon'] = abs(df.LongitudeDec - df.LongitudeDec.shift(1))
df['below_Lat'] = abs(df.LatitudeDec - df.LatitudeDec.shift(-1))
df['above_Lat'] = abs(df.LatitudeDec - df.LatitudeDec.shift(1))

#value to filter out the outliers (can be done better then just using two times the average)
y = df.below_Lon.mean() * 2
x = df.above_Lon.mean() * 2
h = df.below_Lat.mean() * 2
j = df.above_Lat.mean() * 2

#create dataframes of outliers and surrounding values
LongOut1 = df[df.below_Lon > y]
LongOut2 = df[df.above_Lon > x]
LatOut1 = df[df.below_Lat > h]
LatOut2 = df[df.above_Lat > j]

#combines the dataframe and takes only the rownumbers that are in both dataframes (the 1 and 2)
result_Lon = LongOut1.merge(LongOut2, how = 'inner')
result_Lat = LatOut1.merge(LatOut2, how = 'inner')
result = result_Lon.append(result_Lat)
result #all the outliers

#so now we know which LRP's are outliers and we could delete them or replace them by another value in the datafame
#tried a few things to delete them, did not work yet. 