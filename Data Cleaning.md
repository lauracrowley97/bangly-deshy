# bangly-deshy
Consider cleaning Road data (RMMS) first (before bridges etc as this may fix some of the bridge errors)
Start with quick scan of Rid.detail.htm: overview file with summary data, to get an idea of what data about bridges is included.
When cleaning data, start with the original files from Ministry (some of the files given are prepared from the originals, and will contain even more data).  With "original database file RMMS/N1.lrps.ht" create a script that:
 1. Takes in the data into one array for each column/road/etc. (maybe open in text Editor first to see the formatting of .ht)
 2. Keeps a log (not just prints...but a specific function in most languages) of changes i.e. an output file with any alterations made.
 3. In an array that contains all the coordinaets for a road (in the correct order!! - this may be a source of error?) , compare each coordinate to the average of those before and after it. (Averaging is a good estimate in this case as the plotted points are so close together - a more accurate could be a weighted average of the change in angles of the preceeding points on the road i.e. like a smoothing fucntion that predicts path trajectories - but I think an average is just as good an estimate in this data?)
 4. define some threshold (as a MACRO variable maybe?) and if the coordinate differs from the expected value (the average) by this threshold, change it to the value of the average (and LOG the change).
 5. at the end of the script make sure to write all the data back to some file with a new name so as not to overwrite the old data that was cleaned.
 6 have a "human" look at the change log, maybe see if the 'threshold' is too high/low...if not sure, visualise on map to see any obvious errors.
 7. now the other files that were provided for us, but which were generated from the ministry data (that we have now cleaned), need to be regenerated. This includes bridge files (I think?)
 
 
 Secondly, the bridge data (BMMS) needs to be cleaned, which is slightly more complicated perhaps. Again, an initial scan of the data provided is useful to see what fields are provided, and the structure they are in. ( I think there is some field in each bridge data about which road it belongs too - if not, this method is pretty useless.. :( )
 1. Again, write in the data from the original Ministry files, into arrays/matrix/whateva in a script. The ".htm" files, and the Rid.widths.txt file are raw files that come directly from the Ministry of Transpprt.
 2. Make a loop that iterates through one road at a time (would be usefull to have a dictionary/array that just contains a Key Identifier of all the roads, and nothing else).
 3. Considering a single road at a time, iterate through each bridge that also matches this Key Identifier in their "which road does this bridge belong to?" field.
 4. Again, need some threshold value for which, if the coordinates of the bridge are farther away from this threshold to the closest coordinate of the road...Log this bridge as a potential error.
 5. At first, simply get an idea of how many such bridges we are dealing with - if very small...correct all - if too large...filter out the unused bridges (delete those) and fix the frequently used ones (logging any deleted bridges ! ).
 6. Suggestions for fixing: manually by looking up the name in GoogleMaps and coorecting the co-ordinates.
 Automatically, by ?? not sure yet...lets see when we know what kind of errors are occuring.
 7. Might be a good idea that any bridges that are incorrect, and also used very very frequently...get automatically sent to a Log that requires a human to fix manually?
 
 Third major problem we might encournter is that a string of bridges exits, where no road is recorded...maybe first or second part of data cleaning will fix this? If not, they may appear in the error log for the above bridge cleaning script. Maybe, if these bridges are being iterated through in their physical order, and 3 or more are reported as incorrect in a row...create a separete Log that bundles all the preceeding bridges with consecutive errors as a 'missing road for a series of bridges' type array. And this can identify them properly, instead of lumping these in with all the generic errors for random bridges being in the wrong place due to a messed up coordinate.
