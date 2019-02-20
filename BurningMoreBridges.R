#this script requires that BMMMS_overview.xls is resaved as a .csv file in the same location within the same BMMS file in your working directory.
#install.packages("geosphere")     --> only avaailable for most recent version of R so check R.version up to date
library(biogeo)

#think about adding two more cleaning:
#   1. check unique of roadnames in bridge set against roadnames in road data set to find missing entire roads
#   2. check unique of bridges (ie. same lrp number and some other field) to find duplicates in bridge data

#chnage log documents the brigde id and the type of change
change_log <- list('change_log')

#Would prefere to restrict these to static only - how to do in R?
#..NEED TO DEFINE THESE MORE INTUITIVELY
#would be nice to run 'experiments' with these thresholds as controls
threshold_match <- 20  #how close does a point have to be for an 'exact match' UNITS: metres
threshold_chainage <- 10 #meters 'how close does the chainage difference have to be?'
threshold_interpolate <- 200 #meters 'last resort: how close do 2 side by side points have to be fro interpolation?'

#read in bridge data - making sure it has been saved as a .csv
bridge_data <- read.csv('BMMS/BMMS_overview.csv', header = TRUE)
bridge_data <- bridge_data[order(bridge_data$road),] #ordered by road number so it corresponds to our list of roads


road_list <- read.csv(file = "_roadnames_list.csv", header = FALSE)
#BIGGEST FOR LOOP HERE CYCLING THROUGH EACH ROAD
i=0
while(bridge_data$road == road_list[i]) { 

for (row in 1:nrow(bridge_data)) { 
#2nd BIGGEST FOR LOOP HERE CYCLING THROUGH EACH BRIDGE ON THE ROAD
#variables THAT NEED TO BE IMPORTED FROM BMMS_Overview.csv TO BE WRITTEN !!!
bridge_lrp <- toString(bridge_data[row, "LRPName"])         #this is the lrp name and not the structure id
bridge_chainage  <- bridge_data[row,"chainage"]    #in metres
lat_bridge    <- bridge_data[row,"lat"]      #in degrees decimal
lon_bridge   <- bridge_data[row,"lon"] 
estimated_loc <-  toString(bridge_data[row, "EstimatedLoc"])
#these all need to be rewritten after changes


#to store the 2 closest lrp points found to possibly use for interpolation if no exact match
closest_lrps <- matrix( nrow = 2,ncol = 2) 

#3rd BIGGEST FOR LOOP HERE CYCLING THROUGH EACH LRP POINT ON THE ROAD
for (lrp in road_data) {

#variables that need to be imported from csv output of road data cleaning script
lrp_roadpoint   #the id of the lrp on the road
road_chainge
lat_roadpoint <- c(0,0,0)
lon_roadpoint <- c(0,0,0)


#calculate difference in chainage for the bridge and every lrp point on the road - could get a match!
chainage_diff <- abs(lrp_chainage - road_chainage) ##Shouldn't this be bridge_chainage instead of lrp_chainage? lrp_chainage is not defined anywhere
#big thoughts: if chainage was never updated after maintanence, for the road point, then this won't cause an error as the lrp name will 
#still match an lrp name on the road --- (which we are checking for very wrong chaiange records) -- and if updated according to the location of that
#LRP point - in this case the chainage may still be incorrect in the bridge -- is this ever used agaiN? do we need to check for this case and update
#when it's inconsistent...thoughts?


#first check for an exact match of lrp identifier numbers
if (lrp_roadpoint == bridge_lrp){
  estimated_loc <- 'bsc1'
  if (! (lat_bridge == lat_roadpoint && lon_bridge == lon_bridge)){ 
    #need to update
    lat_bridge <- lat_roadpoint
    lon_bridge <- lon_roadpoint
    
    estimated_loc <- 'road_precise'
    #log changes: 
    change_log[length(change_log) +1] <- paste('Bridge number ', bridge_lrp,' changed: precise match with lrp point')
    break ##is this the correct - or exit -- maybe need a flag and a loop :<
  }
  
} else if (distm(c(lon_bridge, lat_bridge), c(lon_roadpoint, lat_roadpoint), fun = distHaversine) < threshold_match) 
  { #returns the distance in metres between 2 coordinates
  lat_bridge <- lat_roadpoint
  lon_bridge <- lon_roadpoint
  
  estimated_loc <- 'road_imprecise'
  #log changes: 
  change_log[length(change_log) +1] <- paste('Bridge number ', bridge_lrp,' changed: Close match with lrp point')
  break ##is this the correct - or exit -- maybe need a flag and a loop :<
  
} else if(chainage_diff <= threshold_chainage){
  lat_bridge <- lat_roadpoint
  lon_bridge <- lon_roadpoint
  
  estimated_loc <- 'road_chainage'
  #log changes: 
  change_log[length(change_log) +1] <- paste('Bridge number ', bridge_lrp,' changed: Close match with lrp chainage')
  break ##is this the correct - or exit -- maybe need a flag and a loop :<
  

}else if (chainage_diff < threshold_interpolate)
{ #it might be close enough to be one of the 'closest points' of the road to the bridge co-ordinates
  #closest_lrps list stores the closest as index 1 and the second closest as index 2 always
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

}
#END OF 3rd BIGGEST LOOP CYCLING THROUGH EACH LRP POINT ON THE ROAD


#if nothing else matched closely enough, check if there were any 'closest_lrps' recorded that can be interpolatded
if (! NA %in% closest_lrps ) {
  #if there are points available for intrepolation...do it :) ie. if that matrix is not empty
  lat_bridge <- (closest_lrps[1,1] + closest_lrps[2,1]) /2
  lon_bridge <- (closest_lrps[1,2] + closest_lrps[2,2]) /2
  
  estimated_loc <- 'road_interpolate'
  #log changes: 
  change_log[length(change_log) +1] <- paste('Bridge number ', bridge_lrp,' changed: Interpolation of nearest lrp points.')

  }else {
  #else we have reached the end of our searching, no matches and close lrp points for interpolation have been found so... :'(
  
  estimated_loc <- 'error'
  #what should happen with lat/long in this case? deleted ??? TO BE DISCUSSED WITH GROUP
  change_log[length(change_log) +1] <- paste('Bridge number ', bridge_lrp,' no match found: ERROR/missing data.')
}

}
#END OF 2nd BIGGEST LOOP CYCLING THROUGH EACH BRIDGE ON THE ROAD



i <- i+ 1
}
#END OF BIGGEST LOOP HERE CYCLING THROUGH EACH ROAD

#export change_log --> could be prettier but who cares for now!
write.csv(change_log,file ="change_log.csv")


#export BMMS_Overview.csv
write.csv(bridge_data, file = "BMMS/BMMS_Overview_Cleaned.csv")
