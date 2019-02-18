import pandas as pd

#changes in opening file to find the Roadname 
f =  open("N4.lrps.htm", "rb")
list_road = pd.read_html(f, skiprows = 1)
df_road = list_road[2]
df = df_road.iloc[3:,1:7]
df.columns = ["LRPNo","RoadChainage","LRPType","Description","LatitudeDec","LongitudeDec"]
#pd.to_numeric(df["LatitudeDec"], downcast="integer") #coerce as float
#pd.to_numeric(df["LongitudeDec"], downcast="integer") #coerce as float
df
df['Road'] = str(df_road.iloc[1:2,0:1]).strip('0\n1 LRPs of ,')
df

#converting the output dataframe into the datafame needed to convert to tcv with Robs script
df_csv = df[['Road','LRPNo', 'LatitudeDec', 'LongitudeDec', 'RoadChainage']]
df_csv
