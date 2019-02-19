import pandas as pd

#changes in opening file to find the Roadname 
f =  open("N3.lrps.htm", "rb")
list_road = pd.read_html(f, skiprows = 2)
df_road = list_road[-1]
df_road
df = df_road.iloc[:,1:7]
df.columns = ["LRPNo","RoadChainage","LRPType","Description","LatitudeDec","LongitudeDec"]
df

#converting the output dataframe into the datafame needed to convert to tcv with Robs script
df_csv = df[['Road','LRPNo', 'LatitudeDec', 'LongitudeDec', 'RoadChainage','replaced']]
df_csv

road_cleaned = df[['Road','LRPNo', 'LatitudeDec', 'LongitudeDec', 'RoadChainage','replaced']]