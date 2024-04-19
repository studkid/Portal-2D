-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 19, 2024 at 06:34 PM
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

-- --------------------------------------------------------

--
-- Table structure for table `gameuser`
--

DROP TABLE IF EXISTS `gameuser`;
CREATE TABLE `gameuser` (
  `userID` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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

DROP TABLE IF EXISTS `level`;
CREATE TABLE `level` (
  `levelID` int(11) NOT NULL,
  `levelName` varchar(100) DEFAULT NULL,
  `targetTime` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `level`
--

INSERT INTO `level` (`levelID`, `levelName`, `targetTime`) VALUES
(1, 'Beginner\'s Luck', 15),
(2, 'Trials and Tribulations', 18),
(3, 'The End of the Beginning', 31),
(4, 'The Beginning of the End', 41),
(5, 'Finale', 38);

-- --------------------------------------------------------

--
-- Table structure for table `leveltime`
--

DROP TABLE IF EXISTS `leveltime`;
CREATE TABLE `leveltime` (
  `userID` int(11) NOT NULL,
  `levelID` int(11) NOT NULL,
  `completionTime` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `leveltime`
--

INSERT INTO `leveltime` (`userID`, `levelID`, `completionTime`) VALUES
(30, 1, 9),
(30, 2, 33);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `gameuser`
--
ALTER TABLE `gameuser`
  ADD PRIMARY KEY (`userID`);

--
-- Indexes for table `level`
--
ALTER TABLE `level`
  ADD PRIMARY KEY (`levelID`);

--
-- Indexes for table `leveltime`
--
ALTER TABLE `leveltime`
  ADD PRIMARY KEY (`userID`,`levelID`),
  ADD KEY `userID_FK` (`userID`),
  ADD KEY `levelID_FK` (`levelID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `gameuser`
--
ALTER TABLE `gameuser`
  MODIFY `userID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;

--
-- AUTO_INCREMENT for table `level`
--
ALTER TABLE `level`
  MODIFY `levelID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
