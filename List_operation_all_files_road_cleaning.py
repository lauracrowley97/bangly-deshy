# doing all files together
roadnames = pd.read_csv('_roadnames_list.csv')
roadnames_list = list(roadnames.columns.unique())
for roadname in roadnames_list:
   filename = "{}.lrps.htm".format(roadname)
   f =  open(filename, "rb")
   list_road = pd.read_html(f, skiprows = 4)
   df_road = list_road[2]
   df = df_road.iloc[:,1:7]
   print(df.iloc[0])
