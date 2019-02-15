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

#Get the Mean and Standard Dev from the Lon and Lat
LonMean = df.LongitudeDec.mean()
LatMean = df.LatitudeDec.mean()
LonStd = df.LongitudeDec.std()
LatStd = df.LatitudeDec.std()

#df['LonPlus1'] = df.LongitudeDec.shift(1)
#df['LonMin1'] = df.LongitudeDec.shift(-1)
#df.head()

# below commented out to be replaced by next section (with list comprehension)
df[abs(df.LongitudeDec - df.LongitudeDec.shift(-1)) > LonStd]
df[abs(df.LongitudeDec - df.LongitudeDec.shift(1)) > LonStd]

#list comprehension
#[ expression for item in list if conditional ]
#df_outliers = [(abs(row - row.shift(-1)) > LonStd) for row in df.LongitudeDec]
#take distance betwen point and point after it
#take std dev o those distances
#make range of distances between points thats acceptable
#check distance between point and point after it against range, marking where it's too large
df_distances_lon = [abs(df.LongitudeDec - df.LongitudeDec.shift(-1)) for row in df.LongitudeDec]
df_distances_lon = df_distances_lon[0]
df_distances_lon_std = df_distances_lon.std()

df_outliers = [(abs(df.LongitudeDec - df.LongitudeDec.shift(-1)) > LonStd) for row in df.LongitudeDec]
df_outliers = pd.DataFrame(df_outliers)
df_outliers.to_csv("/Users/castanos/Documents/06 Graduate TU Delft/2018 Q3 Discrete/outliers.csv", sep='\t')