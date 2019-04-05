-- MySQL dump 10.13  Distrib 8.0.15, for macos10.14 (x86_64)
--
-- Host: 127.0.0.1    Database: epa1351group14
-- ------------------------------------------------------
-- Server version	8.0.15

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `brokenbridges`
--

DROP TABLE IF EXISTS `brokenbridges`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `brokenbridges` (
  `RowID3` int(11) NOT NULL,
  `BridgeID` varchar(45) DEFAULT NULL,
  `TimeBroken` double DEFAULT NULL,
  PRIMARY KEY (`RowID3`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `brokenbridges`
--

LOCK TABLES `brokenbridges` WRITE;
/*!40000 ALTER TABLE `brokenbridges` DISABLE KEYS */;
/*!40000 ALTER TABLE `brokenbridges` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hourlyupdate`
--

DROP TABLE IF EXISTS `hourlyupdate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `hourlyupdate` (
  `RowID1` int(11) NOT NULL,
  `SimioHour` double DEFAULT NULL,
  PRIMARY KEY (`RowID1`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hourlyupdate`
--

LOCK TABLES `hourlyupdate` WRITE;
/*!40000 ALTER TABLE `hourlyupdate` DISABLE KEYS */;
INSERT INTO `hourlyupdate` VALUES (1,1.35),(2,3),(3,4),(4,3),(5,6),(7,8),(8,2),(9,8);
/*!40000 ALTER TABLE `hourlyupdate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `segmenttraveltimes`
--

DROP TABLE IF EXISTS `segmenttraveltimes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `segmenttraveltimes` (
  `RowID2` int(11) NOT NULL,
  `LRPName` varchar(45) DEFAULT NULL,
  `VehicleType` varchar(45) DEFAULT NULL,
  `SegTime` double DEFAULT NULL,
  PRIMARY KEY (`RowID2`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `segmenttraveltimes`
--

LOCK TABLES `segmenttraveltimes` WRITE;
/*!40000 ALTER TABLE `segmenttraveltimes` DISABLE KEYS */;
INSERT INTO `segmenttraveltimes` VALUES (1,'2','Truck',2),(2,'4','Car',5);
/*!40000 ALTER TABLE `segmenttraveltimes` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-04-05 16:27:44
