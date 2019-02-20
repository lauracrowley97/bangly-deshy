#install.packages("rlist")
#install.packages("tidyr")
library(rlist)
#library(tidyr)


df <- read.csv('cleaned_all_road_data.csv',sep = '\t', header = T, stringsAsFactors = FALSE)
library('rlist')
#colnames(df)[which(names(df) == "ï..road")] <- "road"
columns <- c("Road", "LRPNo", "LatitudeDec", "LongitudeDec") #update this
df <- df[columns]
#df[,3] <- as.numeric(df[,3])
road_list <- unique(df$Road)

#spread(df, key = numbers, value = value)

#m1 <- t(df)
#d2 <- data.frame(r1=row.names(m1), m1, row.names = NULL)

for (road in road_list) {
  #road = "N1"
  roaddata = list()
  roaddata <- list.append(road)
  df_t <- df[df$Road == road, ]
  df_t <- df_t[order(df_t[,'Road']), ]
  for (i in 1:nrow(df_t)) {
    roaddata <- list.append(roaddata, df_t[i,2], df_t[i,3], df_t[i,4])
  }
  write(roaddata, file = "data.tcv", ncolumns = length(roaddata), append = TRUE, sep = "\t")
}
