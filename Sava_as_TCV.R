#install.packages("rlist")
library(rlist)



df <- read.csv('cleaned_all_road_data.csv',sep = '\t', header = T)
df$LRPNo <- toString(df['LRPNo'])
colnames(df)[which(names(df) == "ï..road")] <- "road"
columns <- c("road", "LRPName", "lat", "lon") #update this
df <- df[columns]
df[,3] <- as.numeric(df[,3])
road_list <- unique(df$road)

for (road in road_list) {
  roaddata = list()
  roaddata <- list.append(road)
  df_t <- df[df$road == road, ]
  for (i in 1:nrow(df_t)) {
    roaddata <- list.append(roaddata, toString(df_t[i,2]), df_t[i,3], df_t[i,4])
  }
  write(roaddata, file = "data.tcv", ncolumns = length(roaddata), append = TRUE, sep = "\t")
}
