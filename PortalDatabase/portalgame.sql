-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 25, 2024 at 03:23 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `portalgame`
--
CREATE DATABASE IF NOT EXISTS `portalgame` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `portalgame`;

DROP TABLE IF EXISTS `leveltime`;
DROP TABLE IF EXISTS `gameuser`;
DROP TABLE IF EXISTS `level`;

-- --------------------------------------------------------

--
-- Table structure for table `gameuser`
--

CREATE TABLE IF NOT EXISTS `gameuser` (
  `userID` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`userID`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `gameuser`
--

INSERT INTO `gameuser` (`userID`, `username`, `password`) VALUES
(30, 'Admin', 'c1c224b03cd9bc7b6a86d77f5dace40191766c485cd55dc48caf9ac873335d6f'),
(31, 'testguy', '10e45d1d6e046e3a9040d5aa5649f972dd9a54ba1245d2249fdba7cd8f9a8947'),
(32, 'Joe', '6dd8b7d7d3c5c4689b33e51b9f10bc6a9be89fe8fa2a127c8c6c03cd05d68ace');

-- --------------------------------------------------------

--
-- Table structure for table `level`
--

CREATE TABLE IF NOT EXISTS `level` (
  `levelID` int(11) NOT NULL AUTO_INCREMENT,
  `levelName` varchar(100) DEFAULT NULL,
  `targetTime` int(11) DEFAULT NULL,
  PRIMARY KEY (`levelID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `leveltime`
--

CREATE TABLE IF NOT EXISTS `leveltime` (
  `userID` int(11) NOT NULL,
  `levelID` int(11) NOT NULL,
  `completionTime` int(11) DEFAULT NULL,
  KEY `userID_FK` (`userID`),
  KEY `levelID_FK` (`levelID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `leveltime`
--
ALTER TABLE `leveltime`
  ADD CONSTRAINT `levelID_FK` FOREIGN KEY (`levelID`) REFERENCES `level` (`levelID`),
  ADD CONSTRAINT `userID_FK` FOREIGN KEY (`userID`) REFERENCES `gameuser` (`userID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
