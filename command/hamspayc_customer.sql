-- phpMyAdmin SQL Dump
-- version 4.9.7
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Mar 04, 2023 at 07:03 AM
-- Server version: 10.5.19-MariaDB-cll-lve
-- PHP Version: 7.4.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `hamspayc_customer`
--

-- --------------------------------------------------------

--
-- Table structure for table `cars`
--

CREATE TABLE `cars` (
  `cid` int(11) NOT NULL,
  `ctype` varchar(100) NOT NULL,
  `plate` varchar(100) NOT NULL,
  `status` varchar(100) NOT NULL DEFAULT 'Vacant',
  `did` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `cars`
--

INSERT INTO `cars` (`cid`, `ctype`, `plate`, `status`, `did`) VALUES
(2, 'Toyota', 'UAB 678K', 'Booked', '793971'),
(4, 'VW', 'UAU537P', 'Vacant', '');

-- --------------------------------------------------------

--
-- Table structure for table `contacts`
--

CREATE TABLE `contacts` (
  `cid` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `message` text NOT NULL,
  `date_time` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `departments`
--

CREATE TABLE `departments` (
  `id` int(11) NOT NULL,
  `dname` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `departments`
--

INSERT INTO `departments` (`id`, `dname`) VALUES
(3, 'Science');

-- --------------------------------------------------------

--
-- Table structure for table `drivers`
--

CREATE TABLE `drivers` (
  `did` varchar(20) NOT NULL,
  `full_name` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `phone` varchar(50) NOT NULL,
  `role` varchar(100) NOT NULL,
  `otp` varchar(20) NOT NULL,
  `expires_in` varchar(20) NOT NULL,
  `plain_password` varchar(50) NOT NULL,
  `location` varchar(100) NOT NULL,
  `license` varchar(100) NOT NULL,
  `car` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `drivers`
--

INSERT INTO `drivers` (`did`, `full_name`, `email`, `password`, `phone`, `role`, `otp`, `expires_in`, `plain_password`, `location`, `license`, `car`) VALUES
('14', 'Kakensa', 'bbagarukayo5@gmail.com', '7c4a8d09ca3762af61e59520943dc26494f8941b', '+256773155093', 'Driver', '40751', '1676550944', '123456', 'Kampala, Uganda', '219218912921', '3'),
('512485', 'Charles', 'charles.bravo@gmail.com', 'd033e22ae348aeb5660fc2140aec35850c4da997', '+256758169837', 'Driver', '26793', '1', '123456', 'Kampala, Uganda', '8278122112', '2'),
('793971', 'Atwijuka', 'atwijuka@gmail.com', '40bd001563085fc35165329ea1ff5c5ecbdbbeef', '', 'Driver', '62893', '1', '123', 'Kampala', '234567890', '2');

-- --------------------------------------------------------

--
-- Table structure for table `gallery`
--

CREATE TABLE `gallery` (
  `id` int(11) NOT NULL,
  `image` varchar(100) NOT NULL,
  `caption` text NOT NULL,
  `date_added` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `gallery`
--

INSERT INTO `gallery` (`id`, `image`, `caption`, `date_added`) VALUES
(5, '475565985.jpg', 'Capture fisheries', '2021-12-14'),
(8, '692571305.jpg', 'Fish trading', '2021-12-14'),
(9, '585854485.jpg', 'Fish farming', '2021-12-14');

-- --------------------------------------------------------

--
-- Table structure for table `notifications`
--

CREATE TABLE `notifications` (
  `nid` int(11) NOT NULL,
  `user` varchar(20) NOT NULL,
  `location` varchar(100) NOT NULL,
  `message` text NOT NULL,
  `response` text NOT NULL,
  `date_added` varchar(100) NOT NULL,
  `coordinates` varchar(100) NOT NULL,
  `driver` varchar(20) NOT NULL,
  `status` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `notifications`
--

INSERT INTO `notifications` (`nid`, `user`, `location`, `message`, `response`, `date_added`, `coordinates`, `driver`, `status`) VALUES
(6, '3750670034', 'Kampala Uganda', 'Hello notification', 'Coming shortly', '2022-10-14 18:16:26', '', '512485', 'Cleared');

-- --------------------------------------------------------

--
-- Table structure for table `patients`
--

CREATE TABLE `patients` (
  `pid` varchar(20) NOT NULL,
  `name` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `phone` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `age` int(11) NOT NULL,
  `address` varchar(250) NOT NULL,
  `otp` varchar(20) NOT NULL,
  `expires_in` varchar(100) NOT NULL DEFAULT '0',
  `image` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `patients`
--

INSERT INTO `patients` (`pid`, `name`, `email`, `phone`, `password`, `age`, `address`, `otp`, `expires_in`, `image`) VALUES
('1409566957', 'Kakensa', 'bagarukayobruce@gmail.com', '+256783169170', '66dabb35ee7d59b93269a25c4436f45f3642cd5d', 18, 'Mbarara Uganda', '73693', '0', ''),
('2', 'Kakensa', 'kakensa30@gmail.com', '+256773155093', 'd033e22ae348aeb5660fc2140aec35850c4da997', 18, 'Mbarara Uganda', '31755', '1665751602', ''),
('3750670034', 'Kakensa', 'bbagarukayo5@gmail.com', '+256758169834', '66dabb35ee7d59b93269a25c4436f45f3642cd5d', 18, 'Mbarara Uganda', '20243', '1666183373', 'https://abcjcharles.com/static/uploads/3083909.jpeg'),
('6764159857', 'Kakensa', 'inno@gmail.com', '+256783169171', '66dabb35ee7d59b93269a25c4436f45f3642cd5d', 18, 'Mbarara Uganda', '37773', '1665959686', ''),
('7666735879', 'Innocent', 'travy@gmail.com', '234567', '7c222fb2927d828af22f592134e8932480637c0d', 18, 'Kampala', '10831', '0', '');

-- --------------------------------------------------------

--
-- Table structure for table `stories`
--

CREATE TABLE `stories` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` text NOT NULL,
  `date_added` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `stories`
--

INSERT INTO `stories` (`id`, `name`, `description`, `date_added`) VALUES
(10, 'Gillnets', '<p>Gillnets&nbsp;are currently a major and popular&nbsp;fishing gear&nbsp;widely used for fish capture in the major and minor water bodies. They are normally set at dusk and hauled in at dawn. Drift gillnetting is commonly practised on&nbsp;Lake Albert, but rarely on other water bodies. The target fish species for the gill net fishery are&nbsp;Nile Perch,&nbsp;Tilapia&nbsp;species,&nbsp;Bagrus,&nbsp;Clarias,&nbsp;Protopterus,&nbsp;Alestes,&nbsp;Hydrocynus&nbsp;and many other demersal species.</p>\r\n\r\n<p>Fish nets&nbsp;have different sizes. The small sized nets are used for fishing small fish while the big sized nets are used for fishing large fish. For instance, half inch up to one inch grade nets are used for fishing Nkejje, one inch up to 6 inch grade for fishing tilapia, and above 6 inch for Nile perch. The fishermen use boats to haul the nest. The bigger the boat, the larger the volume of fish. One net can weigh up to 10&nbsp;kg, without fish. A small boat may not be able to handle such a load.</p>\r\n', '2022-02-06'),
(11, 'Fish-traps, baskets and Weirs', '<p>Various designs of fish traps, baskets and weirs are used in fishery. Conical traps are used most commonly for catching fish species e.g. Clarias, Barbus, Schilbe in marshy shallow waters of lakes, rivers and in permanent and seasonal swamps. These are particularly used on River Nile, Lake Kyoga, swamps and other minor lakes. The gear is strategically set as a barrier and fish voluntarily or involuntarily enter it, but their escape is hindered by a special non-return valve or device. Traps set in the river estuaries and papyrus fringes indiscriminately trap fish (Barbus, Alestes, Clarias, Hydrocyrus, Protopterus, Labeo) of all sizes and ages.</p>\r\n', '2022-02-06'),
(12, 'Fishery by perforated plastic basins', '<p>Perforated basins are extensively used mainly for Alestes nurse fishery on Lake Albert. This is an emerging fishery on this lake. These basins are operated waters. Bait in form of dregs of native beer or cassava flour is splattered in water above immersed basins; fish is attracted to feed on bait and is scooped out.</p>\r\n', '2022-02-06'),
(13, 'Hooks', '<p>Hooks are used for fishing but on a small scale. The size of the hook used depends on the type of fish. Hooks have numbers. The lower the number, the bigger the hook. Hooks used for tilapia are from numbers eleven to sixteen. Those for Nile perch are from seven to 10. Lung fish are fished with hooks of numbers six and five. Bigger hooks are used for bigger fish so that they do not break free and swim away. On Lutoboka landing site on&nbsp;Bugala Island&nbsp;in&nbsp;Kalangala District, fishermen use hooks of number 12 to fish Nile perch. 1000 hooks are put in water. Sprat is put on the hook as bait. The hooks are put 5 meters apart. Not all of them get fish. Sometimes the fishermen get 10 to twenty fish of different sizes. The hooks are kept in a wooden chest.</p>\r\n', '2022-02-06');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `userID` int(11) NOT NULL,
  `firstName` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `contact` varchar(50) NOT NULL,
  `role` varchar(100) NOT NULL,
  `reset_code` varchar(20) NOT NULL DEFAULT '0',
  `active` int(11) NOT NULL,
  `plain_password` varchar(50) NOT NULL,
  `location` varchar(100) NOT NULL,
  `license` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`userID`, `firstName`, `email`, `password`, `contact`, `role`, `reset_code`, `active`, `plain_password`, `location`, `license`) VALUES
(3, 'Charles Brendan', 'admin@gmail.com', '21232f297a57a5a743894a0e4a801fc3', '+256787655523', 'admin', '45841', 1, 'admin', '', ''),
(10, 'Aga Khan', 'agakhan@gmail.com', 'e10adc3949ba59abbe56e057f20f883e', '+256773155093', 'Hospital', '', 1, '123456', 'Kampala Road', '2187218912'),
(11, 'Kakensa', 'scheneider@gmail.com', '827ccb0eea8a706c4c34a16891f84e7b', '+256758169832', 'Hospital', '27219', 1, '12345', 'Mukono Jinja High Way', '217129812912');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `cars`
--
ALTER TABLE `cars`
  ADD PRIMARY KEY (`cid`);

--
-- Indexes for table `contacts`
--
ALTER TABLE `contacts`
  ADD PRIMARY KEY (`cid`);

--
-- Indexes for table `departments`
--
ALTER TABLE `departments`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `drivers`
--
ALTER TABLE `drivers`
  ADD PRIMARY KEY (`did`);

--
-- Indexes for table `gallery`
--
ALTER TABLE `gallery`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `notifications`
--
ALTER TABLE `notifications`
  ADD PRIMARY KEY (`nid`);

--
-- Indexes for table `patients`
--
ALTER TABLE `patients`
  ADD PRIMARY KEY (`pid`);

--
-- Indexes for table `stories`
--
ALTER TABLE `stories`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`userID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `cars`
--
ALTER TABLE `cars`
  MODIFY `cid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `contacts`
--
ALTER TABLE `contacts`
  MODIFY `cid` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `departments`
--
ALTER TABLE `departments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `gallery`
--
ALTER TABLE `gallery`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `notifications`
--
ALTER TABLE `notifications`
  MODIFY `nid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `stories`
--
ALTER TABLE `stories`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `userID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
