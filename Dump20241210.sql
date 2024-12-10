CREATE DATABASE  IF NOT EXISTS `niknekpp` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `niknekpp`;
-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: niknekpp
-- ------------------------------------------------------
-- Server version	8.0.37

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `comment`
--

DROP TABLE IF EXISTS `comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comment` (
  `commentID` int NOT NULL AUTO_INCREMENT,
  `message` text NOT NULL,
  `masterID` int NOT NULL,
  `requestID` int NOT NULL,
  `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`commentID`),
  KEY `masterID` (`masterID`),
  KEY `requestID` (`requestID`),
  CONSTRAINT `comment_ibfk_1` FOREIGN KEY (`masterID`) REFERENCES `user` (`userID`),
  CONSTRAINT `comment_ibfk_2` FOREIGN KEY (`requestID`) REFERENCES `request` (`requestID`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comment`
--

LOCK TABLES `comment` WRITE;
/*!40000 ALTER TABLE `comment` DISABLE KEYS */;
INSERT INTO `comment` VALUES (1,'Интересно...',2,1,'2024-12-06 15:54:20'),(2,'Будем разбираться!',3,2,'2024-12-06 15:54:20'),(3,'Сделаем всё на высшем уровне!',3,3,'2024-12-06 15:54:20'),(4,'sdfsdfsdfsdf',2,1,'2024-12-06 15:54:20'),(5,'ddfgdfgdfgdfg',2,6,'2024-12-06 15:54:20'),(6,'sdfsfsdf',2,6,'2024-12-06 15:54:46'),(7,'dfsdfsf',2,6,'2024-12-06 15:55:34'),(8,'dfgdfgdfg',3,6,'2024-12-06 15:57:33');
/*!40000 ALTER TABLE `comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `repairparts`
--

DROP TABLE IF EXISTS `repairparts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `repairparts` (
  `partID` int NOT NULL AUTO_INCREMENT,
  `partName` varchar(100) NOT NULL,
  `partCost` decimal(10,2) NOT NULL,
  `partAmount` int NOT NULL,
  PRIMARY KEY (`partID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `repairparts`
--

LOCK TABLES `repairparts` WRITE;
/*!40000 ALTER TABLE `repairparts` DISABLE KEYS */;
/*!40000 ALTER TABLE `repairparts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `request`
--

DROP TABLE IF EXISTS `request`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `request` (
  `requestID` int NOT NULL AUTO_INCREMENT,
  `startDate` date NOT NULL,
  `orgTechType` varchar(255) NOT NULL,
  `orgTechModel` varchar(255) DEFAULT NULL,
  `problemDescription` text NOT NULL,
  `requestStatus` enum('В процессе ремонта','Готова к выдаче','Новая заявка') NOT NULL,
  `completionDate` date DEFAULT NULL,
  `repairParts` varchar(45) DEFAULT NULL,
  `masterID` int DEFAULT NULL,
  `clientID` int NOT NULL,
  PRIMARY KEY (`requestID`),
  KEY `clientID` (`clientID`),
  KEY `requests_ibfk_1` (`masterID`),
  CONSTRAINT `request_ibfk_1` FOREIGN KEY (`masterID`) REFERENCES `user` (`userID`),
  CONSTRAINT `request_ibfk_2` FOREIGN KEY (`clientID`) REFERENCES `user` (`userID`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `request`
--

LOCK TABLES `request` WRITE;
/*!40000 ALTER TABLE `request` DISABLE KEYS */;
INSERT INTO `request` VALUES (1,'2023-06-06','Компьютер','DEXP Aquilon O286','Перестал работать','В процессе ремонта','2023-01-01','',2,7),(2,'2023-05-05','Компьютер','DEXP Atlas H388','Перестал работать','В процессе ремонта','2023-01-01','',3,8),(3,'2022-07-07','Ноутбук','MSI GF76 Katana 11UC-879XRU черный','Выключается','Готова к выдаче','2023-01-01',NULL,3,9),(4,'2023-08-02','Ноутбук','MSI Modern 15 B12M-211RU черный','Выключается','Новая заявка','2023-01-01','',3,8),(6,'2024-12-06','sdfsd','fsdfsdf','sdfsf','В процессе ремонта',NULL,NULL,2,3);
/*!40000 ALTER TABLE `request` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `userID` int NOT NULL AUTO_INCREMENT,
  `login` varchar(50) NOT NULL,
  `fio` varchar(100) NOT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `password` varchar(255) NOT NULL,
  `type` enum('Администратор','Мастер','Клиент') NOT NULL,
  PRIMARY KEY (`userID`),
  UNIQUE KEY `login` (`login`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'login1','Носов Иван Михайлович','89210563128','pass1','Администратор'),(2,'login2','Ильин Александр Андреевич','89535078985','pass2','Мастер'),(3,'login3','Никифоров Иван Дмитриевич','89210673849','pass3','Клиент'),(6,'login11','Григорьев Семён Викторович','89219567849','pass11','Мастер'),(7,'login12','Сорокин Дмитрий Ильич','89219567841','pass12','Мастер'),(8,'login13','Белоусов Егор Ярославович','89219567842','pass13','Мастер'),(9,'login14','Суслов Михаил Александрович','89219567843','pass14','Мастер'),(10,'login15','Васильев Вячеслав Александрович','89219567844','pass15','Мастер');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'niknekpp'
--

--
-- Dumping routines for database 'niknekpp'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-12-10 14:13:15
