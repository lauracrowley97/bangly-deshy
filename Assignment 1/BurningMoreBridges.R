#this script requires that BMMS_overview.xls is resaved as a .csv file in the same location within the same BMMS file in your working directory.
#install.packages("geosphere")  and ("prodlim")    --> only avaailable for most recent version of R so check R.version up to date
library(biogeo)
library(prodlim)
library (geosphere)


#chnage log documents the brigde id and the type of change
change_log <- list('change_log')
missing_roads_list <- list()

#Would prefere to restrict these to static only - how to do in R?
#...NEED TO DEFINE THESE MORE INTUITIVELY
#would be nice to run 'experiments' with these thresholds as controls
threshold_match <- 10  #how close does a point have to be for an 'exact match' UNITS: metres
threshold_chainage <- 10 #meters 'how close does the chainage difference have to be?'
threshold_interpolate <- 200 #meters 'last resort: how close do 2 side by side points have to be for interpolation?'

#read in bridge data - making sure it has been saved as a .csv
bridge_data <- read.csv('BMMS/BMMS_overview.csv', header = TRUE)
bridge_data <- bridge_data[order(bridge_data$road),] #ordered by road number so it corresponds to our list of roads
bridge_data$keep_row <- TRUE #used to keep track of rows for deletion, default is TRUE
bridge_data$road_exists <- TRUE 
bridge_data$EstimatedLoc <- "not yet"

#read in road_cleaned = df[[‘Road’,‘LRPNo’, ‘LatitudeDec’, ‘LongitudeDec’, ‘RoadChainage’,‘replaced’]]
road_data <- read.csv(file ='cleaned_all_road_data.csv', header = TRUE, sep = '\t')
road_data <- road_data[order(road_data$Road),]
road_data <- road_data[,-9]
road_data<- na.omit(road_data) ##WOULD BE NICE TO REPORT WHICH ONE WAS NANAANANANNANNANA


#   1. check unique of roadnames in bridge set against roadnames in road data set to find missing entire roads
roadlist_BMMS <- unique(as.vector(bridge_data$road))
roadlist_RMMS <-unique(as.vector(road_data$Road))

#now we check for roads in the road dataset that have no matching records in the bridge dataset
for (road in roadlist_RMMS){
  match_found <- FALSE
  for (bridgeRoad in roadlist_BMMS){
    if (road == bridgeRoad){
      match_found <- TRUE
    }
  }
    if (match_found == FALSE){
      missing_roads_list[length(missing_roads_list)+1] <- road
      change_log[length(change_log) +1] <- paste('Road number ', road,". No bridge data for this road exists")
    }
}

#now we also check if there are bridges that have no matching road in the road dataset
for (bridgeRoad in roadlist_BMMS){
  match_found <- FALSE
  for (road in roadlist_BMMS){
    if (road == bridgeRoad){
      match_found <- TRUE
      }
  }
  if (match_found == FALSE){
    for(bridge_road in bridge_data){
      if(bridgeRoad %in% bridge_road){
        bridge_data[bridgeRoad, 'keep_row'] <- FALSE
      
      }
    }
    change_log[length(change_log) +1] <- paste('Road number ', bridgeRoad,". This road has records in the bridge dataset, with no corresponding data in the road dataset.")
    }
}


# not sure we need this anymore
#road_list <- read.csv(file = "_roadnames_list.csv", header = FALSE)

#BIG FOR LOOP ITERATING THROUGH EACH BRIDGE
#for (bridge_row in 1:nrow(bridge_data)) { 
for (bridge_row in 1:nrow(bridge_data)) { 
  if(toString(bridge_data[bridge_row, "EstimatedLoc"]) != 'bsc1'){
  stop <- FALSE
  #is this the right place to re-assign ?


  if (bridge_data[bridge_row,"keep_row"] ==  FALSE | bridge_data[bridge_row, "road_exists"] == FALSE) {
    stop <- TRUE

    break #need this to exit entire loop not just this if ??
  }

if(stop == TRUE){break}
  
  
#get the details of this specific bridge from the dataframe 
bridge_lrp <- toString(bridge_data[bridge_row, "LRPName"])         #this is the lrp name and not the structure id
bridge_chainage  <- bridge_data[bridge_row,"chainage"]*1000    #in metres
lat_bridge    <- bridge_data[bridge_row,"lat"]      #in degrees decimal
lon_bridge   <- bridge_data[bridge_row,"lon"] 
estimated_loc <-  toString(bridge_data[bridge_row, "EstimatedLoc"]) #how was the lat/lon estimated
road_bridgepoint <- toString(bridge_data[bridge_row, "road"])  #find the roadname that the bridge is on
structureNr <- bridge_data[bridge_row, "structureNr"]
#these all need to be rewritten after changes

#check for duplicates
#matched_row <- row.match(structureNr, bridge_data, nomatch = 0)
#if (matched_row != 0 ){ 
    #if it also matches on another
   # if (bridge_data[bridge_row, "constructionYear"] > bridge_data[matched_row, "constructionYear"] ){
   #   bridge_data[matched_row,"keep_row"] <-  FALSE
      #generate change log
   #   change_log[length(change_log) +1] <- paste('Bridge number ', toString(bridge_data[matched_row, "LRPName"]) ,' removed due to duplicate of Bridge number', bridge_lrp)

   # }
   # else {

#      bridge_data[bridge_row,"keep_row"] <-  FALSE
 #     change_log[length(change_log) +1] <- paste('Bridge number ', bridge_lrp ,'on road',road_bridgepoint,' removed due to duplicate of Bridge number', toString(bridge_data[matched_row, "LRPNAme"]))
 #     stop <- TRUE###from overall loop !!! CHECKKKKK
    #}
#} ##NB don't delete it twice 

    #would be nice to check if any NAs in the row

#to store the 2 closest lrp points found to possibly use for interpolation if no exact match
closest_lrps <- matrix( nrow = 2,ncol = 2) 

#3rd BIGGEST FOR LOOP HERE CYCLING THROUGH EACH LRP POINT ON THE ROAD
#for (road_row in 1:nrow(road_data)) {
#stop <- FALSE

road_row <- 1 #initialise counter
while (road_row < nrow(road_data) ) {

#variables that need to be imported from csv output of road data cleaning script
lrp_roadpoint   <- toString(road_data[road_row, "LRPNo"])  #the id of the lrp on the road
road_chainage    <- road_data[road_row, "RoadChainage"]*1000 #get in meters
lat_roadpoint   <- road_data[road_row, "LatitudeDec"]
lon_roadpoint   <- road_data[road_row, "LongitudeDec"]
road_roadpoint <- toString(road_data[road_row, "Road"])



#calculate difference in chainage for the bridge and every lrp point on the road - could get a match!
chainage_diff <- abs(bridge_chainage - road_chainage)
#big thoughts: if chainage was never updated after maintanence, for the road point, then this won't cause an error as the lrp name will 
#still match an lrp name on the road --- (which we are checking for very wrong chaiange records) -- and if updated according to the location of that
#LRP point - in this case the chainage may still be incorrect in the bridge -- is this ever used agaiN? do we need to check for this case and update
#when it's inconsistent...thoughts?



#first check for an exact match of lrp identifier numbers on the same road
if (lrp_roadpoint == bridge_lrp && road_roadpoint == road_bridgepoint){
  estimated_loc <- 'bsc1'
  road_row <-  nrow(road_data) +1
  if (! (lat_bridge == lat_roadpoint && lon_bridge == lon_bridge)){ 
    #need to update
    lat_bridge <- lat_roadpoint
    lon_bridge <- lon_roadpoint
    
    estimated_loc <- 'road_precise'
    #log changes: 
    change_log[length(change_log) +1] <- paste('Bridge number ', bridge_lrp,'on road',road_bridgepoint,' changed: precise match with lrp point')
    ##is this the correct - or exit -- maybe need a flag and a loop :<
  }
  
} else if (distm(c(lon_bridge, lat_bridge), c(lon_roadpoint, lat_roadpoint), fun = distHaversine) < threshold_match) 
  { #returns the distance in metres between 2 coordinates
  lat_bridge <- lat_roadpoint
  lon_bridge <- lon_roadpoint
  #print('road_impresce')
  estimated_loc <- 'road_imprecise'
  #log changes: 
  change_log[length(change_log) +1] <- paste('Bridge number ', bridge_lrp,'on road',road_bridgepoint,' changed: Close match with lrp point')
  #stop <- TRUE##is this the correct - or exit -- maybe need a flag and a loop :<
  road_row <-  nrow(road_data) +1
  
} else if(chainage_diff <= threshold_chainage){
  lat_bridge <- lat_roadpoint
  lon_bridge <- lon_roadpoint
  #print('road_chainge')
  estimated_loc <- 'road_chainage'
  #stop <- TRUE
  road_row <- nrow(road_data) +1
  #log changes: 
  change_log[length(change_log) +1] <- paste('Bridge number ', bridge_lrp,'on road',road_bridgepoint,' changed: Close match with lrp chainage')
  ##is this the correct - or exit -- maybe need a flag and a loop :<
  

}else if (chainage_diff < threshold_interpolate){
  #it might be close enough to be one of the 'closest points' of the road to the bridge co-ordinates
  #closest_lrps list stores the closest as index 1 and the second closest as index 2 always
if (! NA %in% closest_lrps ){ #if the closest_lrps isn't empty:
     if (chainage_diff < closest_lrps[1]){
    
       closest_lrps[2,1] <- closest_lrps[1,1]
       closest_lrps[2,2] <- closest_lrps[1,2]
       closest_lrps[1,1] <- lat_roadpoint
       closest_lrps[1,2] <- lon_roadpoint
     }
     else if (chainage_diff < closest_lrps[2]){
        closest_lrps[2,1] <- lat_roadpoint
        closest_lrps[2,2] <- lon_roadpoint
      }
    }
else if(! NA %in% closest_lrps[1,]){
  closest_lrps[1,1] <- lat_roadpoint
  closest_lrps[1,2] <- lon_roadpoint
}
else {
  closest_lrps[2,1] <- lat_roadpoint
  closest_lrps[2,2] <- lon_roadpoint
}
}



road_row <- road_row +1
} #END OF 3rd BIGGEST LOOP CYCLING THROUGH EACH LRP POINT ON THE ROAD


#if nothing else matched closely enough, check if there were any 'closest_lrps' recorded that can be interpolatded
if (! NA %in% closest_lrps && estimated_loc == 'not yet') {
 #if there are points available for intrepolation...do it :) ie. if that matrix is not empt  
  lat_bridge <- (closest_lrps[1,1] + closest_lrps[2,1]) /2
  lon_bridge <- (closest_lrps[1,2] + closest_lrps[2,2]) /2
  
  estimated_loc <- 'road_interpolate'
  #log changes: 
  change_log[length(change_log) +1] <- paste('Bridge number ', bridge_lrp,' changed: Interpolation of nearest lrp points.')

  }else if (estimated_loc == 'not yet'){
  #else we have reached the end of our searching, no matches and close lrp points for interpolation have been found so... :'(
  #print('should report as an error')
  estimated_loc <- 'error'
  #what should happen with lat/long in this case? deleted ??? TO BE DISCUSSED WITH GROUP
  bridge_data[bridge_row,  "keep_row"] <- FALSE
  change_log[length(change_log) +1] <- paste('Bridge number ', bridge_lrp,'on road',road_bridgepoint,'no match found: ERROR/missing data.')
  } 

#rewrite bridge to data file
bridge_data[bridge_row, "LRPName"] <-  bridge_lrp     #this is the lrp name and not the structure id
bridge_data[bridge_row,"chainage"] <- bridge_chainage/1000  #in metres
bridge_data[bridge_row,"lat"] <-  lat_bridge     #in degrees decimal
bridge_data[bridge_row,"lon"] <- lon_bridge 
bridge_data[bridge_row, "EstimatedLoc"]<- estimated_loc

  }
}
#END OF 2nd BIGGEST LOOP CYCLING THROUGH EACH BRIDGE ON THE ROAD




#subset data to get rid of those that should be removed
bridge_data_clean <- subset(bridge_data, bridge_data$keep_row == TRUE, select = - keep_row)

#export change_log --> could be prettier but who cares for now!
write.csv(change_log,file ="change_log.csv")
write.csv(missing_roads_list, file = "missing_roads_in_bridge_dataset.csv")


#export BMMS_Overview.csv -- need this to be original name, and change name of Og to BMMS_Overview_old
write.csv(bridge_data_clean, file = "BMMS/BMMS_Overview_Cleaned.csv")
