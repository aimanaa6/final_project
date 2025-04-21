CREATE DATABASE  IF NOT EXISTS `kaasp` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `kaasp`;
-- MySQL dump 10.13  Distrib 8.0.40, for macos14 (x86_64)
--
-- Host: localhost    Database: kaasp
-- ------------------------------------------------------
-- Server version	9.1.0

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
-- Table structure for table `branches`
--

DROP TABLE IF EXISTS `branches`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `branches` (
  `branch_id` int NOT NULL AUTO_INCREMENT,
  `branch_name` varchar(100) DEFAULT NULL,
  `location_id` int DEFAULT NULL,
  PRIMARY KEY (`branch_id`),
  KEY `location_id` (`location_id`),
  CONSTRAINT `branches_ibfk_1` FOREIGN KEY (`location_id`) REFERENCES `locations` (`location_id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `branches`
--

LOCK TABLES `branches` WRITE;
/*!40000 ALTER TABLE `branches` DISABLE KEYS */;
INSERT INTO `branches` VALUES (1,'Battersea',1),(2,'Chelsea',1),(3,'Fallowfield',2),(4,'Media City',2),(5,'Stratford',1),(6,'Hampstead',1),(7,'Stockwell',1),(8,'Northern Quarter',2),(9,'Salford Quays',2),(10,'Withington',2),(11,'Cardiff',3),(12,'Swansea',3),(13,'Abeerden',4),(14,'Edinburgh',4),(15,'Glasgow',4),(16,'Belfast',5),(17,'London Derry',5);
/*!40000 ALTER TABLE `branches` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `colours`
--

DROP TABLE IF EXISTS `colours`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `colours` (
  `colour_id` int NOT NULL AUTO_INCREMENT,
  `colour_name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`colour_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `colours`
--

LOCK TABLES `colours` WRITE;
/*!40000 ALTER TABLE `colours` DISABLE KEYS */;
INSERT INTO `colours` VALUES (1,'Red'),(2,'Orange'),(3,'Yellow'),(4,'Green'),(5,'Blue'),(6,'Violet'),(7,'Pink');
/*!40000 ALTER TABLE `colours` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contactus`
--

DROP TABLE IF EXISTS `contactus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `contactus` (
  `query_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(100) DEFAULT NULL,
  `subject_id` int DEFAULT NULL,
  `message` varchar(250) DEFAULT NULL,
  `date` date DEFAULT (curdate()),
  `customer_id` int DEFAULT NULL,
  PRIMARY KEY (`query_id`),
  KEY `subject_id` (`subject_id`),
  KEY `fk_customer_id` (`customer_id`),
  CONSTRAINT `contactus_ibfk_1` FOREIGN KEY (`subject_id`) REFERENCES `subjects` (`subject_id`),
  CONSTRAINT `fk_customer_id` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contactus`
--

LOCK TABLES `contactus` WRITE;
/*!40000 ALTER TABLE `contactus` DISABLE KEYS */;
INSERT INTO `contactus` VALUES (1,'benicio_m',3,'Test 1000','2025-04-18',2);
/*!40000 ALTER TABLE `contactus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customers`
--

DROP TABLE IF EXISTS `customers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customers` (
  `customer_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(100) DEFAULT NULL,
  `first_name` varchar(100) DEFAULT NULL,
  `last_name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`customer_id`),
  UNIQUE KEY `unique_username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customers`
--

LOCK TABLES `customers` WRITE;
/*!40000 ALTER TABLE `customers` DISABLE KEYS */;
INSERT INTO `customers` VALUES (1,'aisha_k','Aisha','Khan','aisha.khan@example.com','$2b$12$64mGvrGkcmbhkhEQZhjZEOJeHxRN1DliUwFqZfMrQ74kIqkoF7lnS'),(2,'benicio_m','Benicio','Martinez','benicio.martinez@example.com','$2b$12$feZG6odqvsbeIgpnlD8kOuM9YEesFampXmtODkHFJ6cyvMlHCSixG');
/*!40000 ALTER TABLE `customers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `locations`
--

DROP TABLE IF EXISTS `locations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `locations` (
  `location_id` int NOT NULL AUTO_INCREMENT,
  `location_name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`location_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `locations`
--

LOCK TABLES `locations` WRITE;
/*!40000 ALTER TABLE `locations` DISABLE KEYS */;
INSERT INTO `locations` VALUES (1,'London'),(2,'Manchester'),(3,'Wales'),(4,'Scotland'),(5,'Nothern Ireland');
/*!40000 ALTER TABLE `locations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products` (
  `product_id` int NOT NULL AUTO_INCREMENT,
  `product_name` varchar(100) DEFAULT NULL,
  `product_description` varchar(250) DEFAULT NULL,
  `price` decimal(3,2) DEFAULT NULL,
  `colour_id` int DEFAULT NULL,
  PRIMARY KEY (`product_id`),
  KEY `colour_id` (`colour_id`),
  CONSTRAINT `products_ibfk_1` FOREIGN KEY (`colour_id`) REFERENCES `colours` (`colour_id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES (1,'Red Velvet Cupcake','Moist red velvet sponge topped with cream cheese frosting',2.50,1),(2,'Strawberry Shortcake','Layers of sponge, strawberries, and whipped cream',3.75,7),(3,'Orange Macaron','Crispy almond shell with orange zest ganache',1.90,2),(4,'Citrus Tart','Tangy orange and lemon curd in a buttery crust',3.20,2),(5,'Lemon Meringue Pie','Classic lemon filling topped with toasted meringue',4.00,3),(6,'Yellow Sunshine Cookie','Buttery cookie with lemon glaze',1.50,3),(7,'Matcha Swirl Brownie','Fudgy brownie with a green tea swirl',2.80,4),(8,'Pistachio Muffin','Light green muffin with pistachio bits',2.60,4),(9,'Blueberry Cheesecake','Rich cheesecake with a blueberry topping',4.25,5),(10,'Blue Macaron','Delicate blue macaron with vanilla cream',1.90,5),(11,'Grape Frosted Donut','Fluffy donut with purple grape icing and sprinkles',2.10,6),(12,'Lavender Shortbread','Fragrant shortbread with a hint of lavender',2.00,6),(13,'Pink Strawberry Donut','Soft yeast donut with strawberry glaze and pink sprinkles',2.20,7),(14,'Pink Croissant','Flaky, buttery croissant with a delicate strawberry glaze',2.80,7),(15,'Red Berry Fizz','Sparkling soda infused with strawberries and raspberries',2.80,1),(16,'Ruby Lemonade','Tart homemade lemonade with a red berry twist',2.50,1),(17,'Orange Cream Soda','Creamy orange soda topped with vanilla foam',2.70,2),(18,'Peach Iced Tea','Refreshing iced tea with juicy peach flavor',2.40,2),(19,'Golden Chai Latte','Spiced chai with turmeric and steamed milk',3.10,2),(20,'Honey Lemon Cooler','Cold lemon drink sweetened with wildflower honey',2.60,3),(21,'Green Apple Sparkler','Fizzy drink with crisp green apple flavor',2.80,4),(22,'Matcha Latte','Creamy Japanese green tea latte',3.50,4),(23,'Blueberry Iced Tea','Cold brewed tea with blueberry infusion',2.70,5),(24,'Blue Lemonade','Sweet and tangy lemonade with a splash of blue curacao (non-alcoholic)',2.90,5),(25,'Purple Grape Soda','Classic grape soda with natural grape essence',2.40,6),(26,'Lavender Milk Tea','Floral milk tea with tapioca pearls',3.00,6),(27,'Pink Lemonade','Sweet lemonade with a hint of raspberry and lemon',2.50,7),(28,'Strawberry Milkshake','Creamy milkshake blended with real strawberries',3.30,7);
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `subjects`
--

DROP TABLE IF EXISTS `subjects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `subjects` (
  `subject_id` int NOT NULL AUTO_INCREMENT,
  `subject_description` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`subject_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `subjects`
--

LOCK TABLES `subjects` WRITE;
/*!40000 ALTER TABLE `subjects` DISABLE KEYS */;
INSERT INTO `subjects` VALUES (1,'Allergy complaint'),(2,'Ingredients question'),(3,'Recipe'),(4,'Bakery feedback'),(5,'Job Posting'),(6,'Culture'),(7,'Sustainability'),(8,'General'),(9,'Product feedback');
/*!40000 ALTER TABLE `subjects` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'kaasp'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-18 10:46:51
