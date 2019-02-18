df_bridges <- read.csv(file = "BMMS_overview.csv", header = T, sep = ';')
df_roads <- read.csv(file = "Roads_InfoAboutEachLRP.csv", header = T, sep = ',')

df_roads_bridges <-df_roads[df_roads$type == 'Bridge' | df_roads$type ==  'Culvert',]

df_merged <- rbind(df_bridges, df_roads_bridges, by.x = 'LRPName', by.y = 'lrp', all.x = TRUE)


for (index in df_bridges) {
  if df_bridges$EstimatedLoc == 'bcs1' {
    
  }
  else if df_bridges$EstimatedLoc == 'road_precise' {
    
  }
  else if df_bridges$EstimatedLoc == 'road_chainage' {
    
  }
  else if df_bridges$EstimatedLoc == 'road_interpolate' {
    
  }
  else if df_bridges$EstimatedLoc == 'error' {
    
  }
  else if df_bridges$EstimatedLoc == 'bcs1_zerosec' {
    
  }
}