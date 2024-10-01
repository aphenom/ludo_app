-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3307
-- Généré le : lun. 30 sep. 2024 à 09:29
-- Version du serveur : 11.3.2-MariaDB
-- Version de PHP : 8.2.18

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `ludo`
--

-- --------------------------------------------------------

--
-- Structure de la table `account_emailaddress`
--

DROP TABLE IF EXISTS `account_emailaddress`;
CREATE TABLE IF NOT EXISTS `account_emailaddress` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(254) NOT NULL,
  `verified` tinyint(1) NOT NULL,
  `primary` tinyint(1) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `account_emailaddress_user_id_email_987c8728_uniq` (`user_id`,`email`),
  KEY `account_emailaddress_email_03be32b2` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `account_emailaddress`
--

INSERT INTO `account_emailaddress` (`id`, `email`, `verified`, `primary`, `user_id`) VALUES
(1, 'amorosomai@yahoo.fr', 0, 1, 1);

-- --------------------------------------------------------

--
-- Structure de la table `account_emailconfirmation`
--

DROP TABLE IF EXISTS `account_emailconfirmation`;
CREATE TABLE IF NOT EXISTS `account_emailconfirmation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created` datetime(6) NOT NULL,
  `sent` datetime(6) DEFAULT NULL,
  `key` varchar(64) NOT NULL,
  `email_address_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `key` (`key`),
  KEY `account_emailconfirmation_email_address_id_5b7f8c58` (`email_address_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Structure de la table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Structure de la table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_group_id_b120cbf9` (`group_id`),
  KEY `auth_group_permissions_permission_id_84c5c92e` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Structure de la table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  KEY `auth_permission_content_type_id_2f476e4b` (`content_type_id`)
) ENGINE=MyISAM AUTO_INCREMENT=101 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Déchargement des données de la table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add email address', 7, 'add_emailaddress'),
(26, 'Can change email address', 7, 'change_emailaddress'),
(27, 'Can delete email address', 7, 'delete_emailaddress'),
(28, 'Can view email address', 7, 'view_emailaddress'),
(29, 'Can add email confirmation', 8, 'add_emailconfirmation'),
(30, 'Can change email confirmation', 8, 'change_emailconfirmation'),
(31, 'Can delete email confirmation', 8, 'delete_emailconfirmation'),
(32, 'Can view email confirmation', 8, 'view_emailconfirmation'),
(33, 'Can add social account', 9, 'add_socialaccount'),
(34, 'Can change social account', 9, 'change_socialaccount'),
(35, 'Can delete social account', 9, 'delete_socialaccount'),
(36, 'Can view social account', 9, 'view_socialaccount'),
(37, 'Can add social application', 10, 'add_socialapp'),
(38, 'Can change social application', 10, 'change_socialapp'),
(39, 'Can delete social application', 10, 'delete_socialapp'),
(40, 'Can view social application', 10, 'view_socialapp'),
(41, 'Can add social application token', 11, 'add_socialtoken'),
(42, 'Can change social application token', 11, 'change_socialtoken'),
(43, 'Can delete social application token', 11, 'delete_socialtoken'),
(44, 'Can view social application token', 11, 'view_socialtoken'),
(45, 'Can add country', 12, 'add_country'),
(46, 'Can change country', 12, 'change_country'),
(47, 'Can delete country', 12, 'delete_country'),
(48, 'Can view country', 12, 'view_country'),
(49, 'Can add region/state', 13, 'add_region'),
(50, 'Can change region/state', 13, 'change_region'),
(51, 'Can delete region/state', 13, 'delete_region'),
(52, 'Can view region/state', 13, 'view_region'),
(53, 'Can add city', 14, 'add_city'),
(54, 'Can change city', 14, 'change_city'),
(55, 'Can delete city', 14, 'delete_city'),
(56, 'Can view city', 14, 'view_city'),
(57, 'Can add SubRegion', 15, 'add_subregion'),
(58, 'Can change SubRegion', 15, 'change_subregion'),
(59, 'Can delete SubRegion', 15, 'delete_subregion'),
(60, 'Can view SubRegion', 15, 'view_subregion'),
(61, 'Can add profil', 16, 'add_profil'),
(62, 'Can change profil', 16, 'change_profil'),
(63, 'Can delete profil', 16, 'delete_profil'),
(64, 'Can view profil', 16, 'view_profil'),
(65, 'Can add partie', 17, 'add_partie'),
(66, 'Can change partie', 17, 'change_partie'),
(67, 'Can delete partie', 17, 'delete_partie'),
(68, 'Can view partie', 17, 'view_partie'),
(69, 'Can add participation', 18, 'add_participation'),
(70, 'Can change participation', 18, 'change_participation'),
(71, 'Can delete participation', 18, 'delete_participation'),
(72, 'Can view participation', 18, 'view_participation'),
(73, 'Can add historique notification', 19, 'add_historiquenotification'),
(74, 'Can change historique notification', 19, 'change_historiquenotification'),
(75, 'Can delete historique notification', 19, 'delete_historiquenotification'),
(76, 'Can view historique notification', 19, 'view_historiquenotification'),
(77, 'Can add transaction', 20, 'add_transaction'),
(78, 'Can change transaction', 20, 'change_transaction'),
(79, 'Can delete transaction', 20, 'delete_transaction'),
(80, 'Can view transaction', 20, 'view_transaction'),
(81, 'Can add observation', 21, 'add_observation'),
(82, 'Can change observation', 21, 'change_observation'),
(83, 'Can delete observation', 21, 'delete_observation'),
(84, 'Can view observation', 21, 'view_observation'),
(85, 'Can add config', 22, 'add_config'),
(86, 'Can change config', 22, 'change_config'),
(87, 'Can delete config', 22, 'delete_config'),
(88, 'Can view config', 22, 'view_config'),
(89, 'Can add mise', 23, 'add_mise'),
(90, 'Can change mise', 23, 'change_mise'),
(91, 'Can delete mise', 23, 'delete_mise'),
(92, 'Can view mise', 23, 'view_mise'),
(93, 'Can add taux commission', 24, 'add_tauxcommission'),
(94, 'Can change taux commission', 24, 'change_tauxcommission'),
(95, 'Can delete taux commission', 24, 'delete_tauxcommission'),
(96, 'Can view taux commission', 24, 'view_tauxcommission'),
(97, 'Can add taux transaction', 25, 'add_tauxtransaction'),
(98, 'Can change taux transaction', 25, 'change_tauxtransaction'),
(99, 'Can delete taux transaction', 25, 'delete_tauxtransaction'),
(100, 'Can view taux transaction', 25, 'view_tauxtransaction');

-- --------------------------------------------------------

--
-- Structure de la table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE IF NOT EXISTS `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, '!jiXsBKuvz7fgKvTzI5uoupfo8W4yueqNIFgCspoM', '2024-09-30 01:45:52.819791', 0, 'amos', 'Amos', 'Phenoom', 'amorosomai@yahoo.fr', 0, 1, '2024-09-26 23:09:44.589607');

-- --------------------------------------------------------

--
-- Structure de la table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE IF NOT EXISTS `auth_user_groups` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_user_id_6a12ed8b` (`user_id`),
  KEY `auth_user_groups_group_id_97559544` (`group_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Structure de la table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE IF NOT EXISTS `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_user_id_a95ead1b` (`user_id`),
  KEY `auth_user_user_permissions_permission_id_1fbb5f2c` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Structure de la table `cities_light_city`
--

DROP TABLE IF EXISTS `cities_light_city`;
CREATE TABLE IF NOT EXISTS `cities_light_city` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name_ascii` varchar(200) NOT NULL,
  `slug` varchar(50) NOT NULL,
  `geoname_id` int(11) DEFAULT NULL,
  `alternate_names` longtext DEFAULT NULL,
  `name` varchar(200) NOT NULL,
  `display_name` varchar(200) NOT NULL,
  `search_names` longtext NOT NULL,
  `latitude` decimal(8,5) DEFAULT NULL,
  `longitude` decimal(8,5) DEFAULT NULL,
  `region_id` int(11) DEFAULT NULL,
  `country_id` int(11) NOT NULL,
  `population` bigint(20) DEFAULT NULL,
  `feature_code` varchar(10) DEFAULT NULL,
  `timezone` varchar(40) DEFAULT NULL,
  `subregion_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `geoname_id` (`geoname_id`),
  UNIQUE KEY `cities_light_city_region_id_subregion_id_name_cdfc77ea_uniq` (`region_id`,`subregion_id`,`name`),
  UNIQUE KEY `cities_light_city_region_id_subregion_id_slug_efb2e768_uniq` (`region_id`,`subregion_id`,`slug`),
  KEY `cities_light_city_name_ascii_1e56323b` (`name_ascii`),
  KEY `cities_light_city_slug_cb2251f8` (`slug`),
  KEY `cities_light_city_name_4859e2a5` (`name`),
  KEY `cities_light_city_region_id_f7ab977b` (`region_id`),
  KEY `cities_light_city_country_id_cf310fd2` (`country_id`),
  KEY `cities_light_city_population_d597eeb6` (`population`),
  KEY `cities_light_city_feature_code_d43c9217` (`feature_code`),
  KEY `cities_light_city_timezone_0fb51b1e` (`timezone`),
  KEY `cities_light_city_subregion_id_0926d2ad` (`subregion_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Structure de la table `cities_light_country`
--

DROP TABLE IF EXISTS `cities_light_country`;
CREATE TABLE IF NOT EXISTS `cities_light_country` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name_ascii` varchar(200) NOT NULL,
  `slug` varchar(50) NOT NULL,
  `geoname_id` int(11) DEFAULT NULL,
  `alternate_names` longtext DEFAULT NULL,
  `name` varchar(200) NOT NULL,
  `code2` varchar(2) DEFAULT NULL,
  `code3` varchar(3) DEFAULT NULL,
  `continent` varchar(2) NOT NULL,
  `tld` varchar(5) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `geoname_id` (`geoname_id`),
  UNIQUE KEY `code2` (`code2`),
  UNIQUE KEY `code3` (`code3`),
  KEY `cities_light_country_name_ascii_648cc5e3` (`name_ascii`),
  KEY `cities_light_country_slug_3707a22c` (`slug`),
  KEY `cities_light_country_continent_e2c412a4` (`continent`),
  KEY `cities_light_country_tld_1fb2faaa` (`tld`),
  KEY `cities_light_country_name_1d61d0d2` (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Structure de la table `cities_light_region`
--

DROP TABLE IF EXISTS `cities_light_region`;
CREATE TABLE IF NOT EXISTS `cities_light_region` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name_ascii` varchar(200) NOT NULL,
  `slug` varchar(50) NOT NULL,
  `geoname_id` int(11) DEFAULT NULL,
  `alternate_names` longtext DEFAULT NULL,
  `name` varchar(200) NOT NULL,
  `display_name` varchar(200) NOT NULL,
  `geoname_code` varchar(50) DEFAULT NULL,
  `country_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `cities_light_region_country_id_name_6e5b3799_uniq` (`country_id`,`name`),
  UNIQUE KEY `cities_light_region_country_id_slug_3dd02103_uniq` (`country_id`,`slug`),
  UNIQUE KEY `geoname_id` (`geoname_id`),
  KEY `cities_light_region_name_ascii_f085cb82` (`name_ascii`),
  KEY `cities_light_region_slug_1653969f` (`slug`),
  KEY `cities_light_region_name_775f9496` (`name`),
  KEY `cities_light_region_geoname_code_1b0d4e58` (`geoname_code`),
  KEY `cities_light_region_country_id_b2782d49` (`country_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Structure de la table `cities_light_subregion`
--

DROP TABLE IF EXISTS `cities_light_subregion`;
CREATE TABLE IF NOT EXISTS `cities_light_subregion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `name_ascii` varchar(200) NOT NULL,
  `slug` varchar(50) NOT NULL,
  `geoname_id` int(11) DEFAULT NULL,
  `alternate_names` longtext DEFAULT NULL,
  `display_name` varchar(200) NOT NULL,
  `geoname_code` varchar(50) DEFAULT NULL,
  `country_id` int(11) NOT NULL,
  `region_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `geoname_id` (`geoname_id`),
  KEY `cities_light_subregion_name_2882337e` (`name`),
  KEY `cities_light_subregion_name_ascii_ecf9a336` (`name_ascii`),
  KEY `cities_light_subregion_slug_43494546` (`slug`),
  KEY `cities_light_subregion_geoname_code_843acdc3` (`geoname_code`),
  KEY `cities_light_subregion_country_id_9b32b484` (`country_id`),
  KEY `cities_light_subregion_region_id_c6e0b71f` (`region_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Structure de la table `core_config`
--

DROP TABLE IF EXISTS `core_config`;
CREATE TABLE IF NOT EXISTS `core_config` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `app_name` varchar(50) NOT NULL,
  `slogan` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `currency` varchar(15) DEFAULT NULL,
  `contact` varchar(100) DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL,
  `sms_api_url` varchar(100) DEFAULT NULL,
  `notification_api_id` varchar(100) DEFAULT NULL,
  `notification_api_key` varchar(100) DEFAULT NULL,
  `notification_api_url` varchar(100) DEFAULT NULL,
  `sms_api_id` varchar(100) DEFAULT NULL,
  `sms_api_key` varchar(100) DEFAULT NULL,
  `email_api_url` varchar(100) DEFAULT NULL,
  `email_api_id` varchar(100) DEFAULT NULL,
  `email_api_key` varchar(100) DEFAULT NULL,
  `transaction_api_url` varchar(100) DEFAULT NULL,
  `transaction_api_id` varchar(100) DEFAULT NULL,
  `transaction_api_key` varchar(100) DEFAULT NULL,
  `logo` varchar(100) NOT NULL,
  `logo_symbol` varchar(100) NOT NULL,
  `favicon` varchar(100) NOT NULL,
  `minimum_retrait` decimal(10,2) DEFAULT NULL,
  `minimum_depot` decimal(10,2) DEFAULT NULL,
  `note_information` longtext DEFAULT NULL,
  `faq` longtext DEFAULT NULL,
  `about` longtext DEFAULT NULL,
  `privacy_policy` longtext DEFAULT NULL,
  `condition_term` longtext DEFAULT NULL,
  `delai_tour` int(10) UNSIGNED DEFAULT NULL CHECK (`delai_tour` >= 0),
  `etat_retrait` tinyint(1) NOT NULL,
  `etat_validation_prealable_retrait` tinyint(1) NOT NULL,
  `etat_depot` tinyint(1) NOT NULL,
  `etat_partie` tinyint(1) NOT NULL,
  `date_creation` datetime(6) NOT NULL,
  `date_modification` datetime(6) DEFAULT NULL,
  `date_validation` datetime(6) DEFAULT NULL,
  `date_suppression` datetime(6) DEFAULT NULL,
  `etat_validation` tinyint(1) NOT NULL,
  `etat_suppression` tinyint(1) NOT NULL,
  `modifie_par_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `core_config_modifie_par_id_082b2ea7` (`modifie_par_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Structure de la table `core_mise`
--

DROP TABLE IF EXISTS `core_mise`;
CREATE TABLE IF NOT EXISTS `core_mise` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `montant` decimal(10,2) DEFAULT NULL,
  `nombre_minimum` int(10) UNSIGNED DEFAULT NULL CHECK (`nombre_minimum` >= 0),
  `observation` longtext DEFAULT NULL,
  `date_creation` datetime(6) NOT NULL,
  `date_modification` datetime(6) DEFAULT NULL,
  `date_validation` datetime(6) DEFAULT NULL,
  `date_suppression` datetime(6) DEFAULT NULL,
  `etat_validation` tinyint(1) NOT NULL,
  `etat_suppression` tinyint(1) NOT NULL,
  `modifie_par_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `core_mise_modifie_par_id_64470099` (`modifie_par_id`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Déchargement des données de la table `core_mise`
--

INSERT INTO `core_mise` (`id`, `montant`, `nombre_minimum`, `observation`, `date_creation`, `date_modification`, `date_validation`, `date_suppression`, `etat_validation`, `etat_suppression`, `modifie_par_id`) VALUES
(1, 500.00, 3, NULL, '2024-09-24 22:04:40.000000', '2024-09-24 22:04:40.000000', '2024-09-24 22:04:40.000000', NULL, 1, 0, NULL),
(2, 1000.00, 2, NULL, '2024-09-24 22:04:40.000000', '2024-09-24 22:04:40.000000', '2024-09-24 22:04:40.000000', NULL, 1, 0, NULL),
(3, 2000.00, 2, NULL, '2024-09-24 22:04:40.000000', '2024-09-24 22:04:40.000000', '2024-09-24 22:04:40.000000', NULL, 1, 0, NULL),
(4, 5000.00, 2, NULL, '2024-09-24 22:06:06.000000', '2024-09-24 22:06:06.000000', '2024-09-24 22:06:06.000000', NULL, 1, 0, NULL),
(5, 10000.00, 2, NULL, '2024-09-24 22:06:06.000000', '2024-09-24 22:06:06.000000', '2024-09-24 22:06:06.000000', NULL, 1, 0, NULL);

-- --------------------------------------------------------

--
-- Structure de la table `core_tauxcommission`
--

DROP TABLE IF EXISTS `core_tauxcommission`;
CREATE TABLE IF NOT EXISTS `core_tauxcommission` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `taux` decimal(10,2) DEFAULT NULL,
  `debut` datetime(6) NOT NULL,
  `fin` datetime(6) DEFAULT NULL,
  `observation` longtext DEFAULT NULL,
  `date_creation` datetime(6) NOT NULL,
  `date_modification` datetime(6) DEFAULT NULL,
  `date_validation` datetime(6) DEFAULT NULL,
  `date_suppression` datetime(6) DEFAULT NULL,
  `etat_validation` tinyint(1) NOT NULL,
  `etat_suppression` tinyint(1) NOT NULL,
  `modifie_par_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `core_tauxcommission_modifie_par_id_eb8d0ccd` (`modifie_par_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Déchargement des données de la table `core_tauxcommission`
--

INSERT INTO `core_tauxcommission` (`id`, `taux`, `debut`, `fin`, `observation`, `date_creation`, `date_modification`, `date_validation`, `date_suppression`, `etat_validation`, `etat_suppression`, `modifie_par_id`) VALUES
(1, 25.00, '2024-09-24 22:07:05.000000', NULL, NULL, '2024-09-24 22:07:05.000000', '2024-09-24 22:07:05.000000', '2024-09-24 22:07:05.000000', NULL, 1, 0, NULL);

-- --------------------------------------------------------

--
-- Structure de la table `core_tauxtransaction`
--

DROP TABLE IF EXISTS `core_tauxtransaction`;
CREATE TABLE IF NOT EXISTS `core_tauxtransaction` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `type` varchar(20) DEFAULT NULL,
  `taux` decimal(10,2) DEFAULT NULL,
  `debut` datetime(6) NOT NULL,
  `fin` datetime(6) DEFAULT NULL,
  `observation` longtext DEFAULT NULL,
  `date_creation` datetime(6) NOT NULL,
  `date_modification` datetime(6) DEFAULT NULL,
  `date_validation` datetime(6) DEFAULT NULL,
  `date_suppression` datetime(6) DEFAULT NULL,
  `etat_validation` tinyint(1) NOT NULL,
  `etat_suppression` tinyint(1) NOT NULL,
  `modifie_par_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `core_tauxtransaction_modifie_par_id_41a67f9c` (`modifie_par_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Structure de la table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE IF NOT EXISTS `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6` (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Structure de la table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=MyISAM AUTO_INCREMENT=26 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Déchargement des données de la table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(2, 'auth', 'permission'),
(3, 'auth', 'group'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(6, 'sessions', 'session'),
(7, 'account', 'emailaddress'),
(8, 'account', 'emailconfirmation'),
(9, 'socialaccount', 'socialaccount'),
(10, 'socialaccount', 'socialapp'),
(11, 'socialaccount', 'socialtoken'),
(12, 'cities_light', 'country'),
(13, 'cities_light', 'region'),
(14, 'cities_light', 'city'),
(15, 'cities_light', 'subregion'),
(16, 'player', 'profil'),
(17, 'player', 'partie'),
(18, 'player', 'participation'),
(19, 'player', 'historiquenotification'),
(20, 'player', 'transaction'),
(21, 'player', 'observation'),
(22, 'core', 'config'),
(23, 'core', 'mise'),
(24, 'core', 'tauxcommission'),
(25, 'core', 'tauxtransaction');

-- --------------------------------------------------------

--
-- Structure de la table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE IF NOT EXISTS `django_migrations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=48 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Déchargement des données de la table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2024-09-21 19:21:35.744570'),
(2, 'auth', '0001_initial', '2024-09-21 19:21:36.125722'),
(3, 'account', '0001_initial', '2024-09-21 19:21:36.223028'),
(4, 'account', '0002_email_max_length', '2024-09-21 19:21:36.247217'),
(5, 'account', '0003_alter_emailaddress_create_unique_verified_email', '2024-09-21 19:21:36.273085'),
(6, 'account', '0004_alter_emailaddress_drop_unique_email', '2024-09-21 19:21:36.646166'),
(7, 'account', '0005_emailaddress_idx_upper_email', '2024-09-21 19:21:36.651200'),
(8, 'account', '0006_emailaddress_lower', '2024-09-21 19:21:36.661164'),
(9, 'account', '0007_emailaddress_idx_email', '2024-09-21 19:21:36.685147'),
(10, 'account', '0008_emailaddress_unique_primary_email_fixup', '2024-09-21 19:21:36.697610'),
(11, 'account', '0009_emailaddress_unique_primary_email', '2024-09-21 19:21:36.703605'),
(12, 'admin', '0001_initial', '2024-09-21 19:21:36.797428'),
(13, 'admin', '0002_logentry_remove_auto_add', '2024-09-21 19:21:36.803023'),
(14, 'admin', '0003_logentry_add_action_flag_choices', '2024-09-21 19:21:36.809027'),
(15, 'contenttypes', '0002_remove_content_type_name', '2024-09-21 19:21:36.856367'),
(16, 'auth', '0002_alter_permission_name_max_length', '2024-09-21 19:21:36.878919'),
(17, 'auth', '0003_alter_user_email_max_length', '2024-09-21 19:21:36.901652'),
(18, 'auth', '0004_alter_user_username_opts', '2024-09-21 19:21:36.908593'),
(19, 'auth', '0005_alter_user_last_login_null', '2024-09-21 19:21:36.933672'),
(20, 'auth', '0006_require_contenttypes_0002', '2024-09-21 19:21:36.934642'),
(21, 'auth', '0007_alter_validators_add_error_messages', '2024-09-21 19:21:36.939689'),
(22, 'auth', '0008_alter_user_username_max_length', '2024-09-21 19:21:36.963940'),
(23, 'auth', '0009_alter_user_last_name_max_length', '2024-09-21 19:21:36.985673'),
(24, 'auth', '0010_alter_group_name_max_length', '2024-09-21 19:21:37.009368'),
(25, 'auth', '0011_update_proxy_permissions', '2024-09-21 19:21:37.016703'),
(26, 'auth', '0012_alter_user_first_name_max_length', '2024-09-21 19:21:37.038141'),
(27, 'sessions', '0001_initial', '2024-09-21 19:21:37.062948'),
(28, 'socialaccount', '0001_initial', '2024-09-21 19:21:37.255544'),
(29, 'socialaccount', '0002_token_max_lengths', '2024-09-21 19:21:37.321511'),
(30, 'socialaccount', '0003_extra_data_default_dict', '2024-09-21 19:21:37.327485'),
(31, 'socialaccount', '0004_app_provider_id_settings', '2024-09-21 19:21:37.421448'),
(32, 'socialaccount', '0005_socialtoken_nullable_app', '2024-09-21 19:21:37.626106'),
(33, 'socialaccount', '0006_alter_socialaccount_extra_data', '2024-09-21 19:21:37.650578'),
(34, 'cities_light', '0001_initial', '2024-09-23 21:15:31.229696'),
(35, 'cities_light', '0002_city', '2024-09-23 21:15:31.479587'),
(36, 'cities_light', '0003_auto_20141120_0342', '2024-09-23 21:15:31.483609'),
(37, 'cities_light', '0004_autoslug_update', '2024-09-23 21:15:31.489677'),
(38, 'cities_light', '0005_blank_phone', '2024-09-23 21:15:31.497316'),
(39, 'cities_light', '0006_compensate_for_0003_bytestring_bug', '2024-09-23 21:15:31.499665'),
(40, 'cities_light', '0007_make_country_name_not_unique', '2024-09-23 21:15:31.989733'),
(41, 'cities_light', '0008_city_timezone', '2024-09-23 21:15:32.029710'),
(42, 'cities_light', '0009_add_subregion', '2024-09-23 21:15:32.251861'),
(43, 'cities_light', '0010_auto_20200508_1851', '2024-09-23 21:15:33.240763'),
(44, 'cities_light', '0011_alter_city_country_alter_city_region_and_more', '2024-09-23 21:15:33.258949'),
(45, 'core', '0001_initial', '2024-09-23 21:15:33.510105'),
(46, 'player', '0001_initial', '2024-09-23 21:15:34.540012'),
(47, 'player', '0002_alter_profil_pays_residence', '2024-09-24 22:27:46.396811');

-- --------------------------------------------------------

--
-- Structure de la table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('1loikft5jd51jmt4s02lddh5w4ldsepf', '.eJxVjEEOwiAQRe_C2pAOQwu4dO8ZCAyDVA0kpV0Z765NutDtf-_9l_BhW4vfOi9-TuIsQJx-txjowXUH6R7qrUlqdV3mKHdFHrTLa0v8vBzu30EJvXxrO4JlTqB5VE5hVgr1QBwgR1aEDrQyzpCZADCnzJbYxGxw4IlII4r3B9clN9U:1sv5U0:9hJyCNI2zwpW6wtdxkl2k_Lu18hr0RXoxcloCl_5J9Q', '2024-10-07 01:45:52.950001'),
('6k2gbh21ghesda53hqzbm31jp35me1s2', '.eJxVj0tuhjAMhO_iNUI4DxLYtdeoKhSMI9BPSUVCN4i7N1C6YGeNvxmPd4iBJjc7orAtqYvJJY7Q7kcB_5rb0shLmsilKSzdF6cxDJn52OFvhvaZAtmboEUjjFbGYl0aXalGF_C9hp9p4DU7vCPuQ3hleJvOCNtYgTY70Iq6Qg3HZwHX8W6LvHYXhPDQekcvXs6Fm-dTLu8K5cXc61i-PV54v12PqNHF8Wyh0TIPqFiLRkgvhFQVsUPfsyDZoBKmMWRqROkHz5bY9N7IimsiJSUcv8Qrb9M:1suc6S:DKwQrWSbzRqJAD4vKhxhyDWIPaTzhCcHYtMkY0w7428', '2024-10-05 18:23:36.766613'),
('jxvybfmih7y93gckxf8vhj1ta3qgzbqe', '.eJw1y7EKwjAQANB_uTmobW0TO-rs4OAgIuFITwmGpCRXDYT8u12cH69ACsaiQ2PC4lknRqYEY4FvvB1yznw5ndVR4RXGe4E5BkNpdXDhZT0ImJARRr84J2B-G9ImTKQ_FO3TUvyLp8xr2kIVjWxlv5dq12yGoe161T1q_QGzTCzf:1suc6D:vjqwR15hnnJ60ie-IzgPv82dJMZjb86fQlwFVkPtEmU', '2024-10-05 18:23:21.664302'),
('sdq8dqtx2b5n3h7ncu5bz1ro3nsaeuqi', '.eJxVj0tuhjAMhO_iNUI4DxLYtdeoKhSMI9BPSUVCN4i7N1C6YGeNvxmPd4iBJjc7orAtqYvJJY7Q7kcB_5rb0shLmsilKSzdF6cxDJn52OFvhvaZAtmboEUjjNbaGFGi0hXqAr7X8DMNvGaHd8R9CK8Mb9MZYRsr0Bqt0Io603B8FnAd77bIa3dBCA-td_Ti5Vy4eT7l8q5QXsy9juXb44X32_WIGl0czxYaLfOAirVohPRCSFURO_Q9C5INKmEaQ6ZGlH7wbIlN742suCZSUsLxC7dob8U:1sueAm:oKLTcnAK-o7eXEY45dfa67m_klz3KJR021L_68Lp1ak', '2024-10-05 20:36:12.157491');

-- --------------------------------------------------------

--
-- Structure de la table `player_historiquenotification`
--

DROP TABLE IF EXISTS `player_historiquenotification`;
CREATE TABLE IF NOT EXISTS `player_historiquenotification` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `objet` varchar(255) DEFAULT NULL,
  `message` longtext DEFAULT NULL,
  `date_creation` datetime(6) NOT NULL,
  `date_modification` datetime(6) DEFAULT NULL,
  `date_validation` datetime(6) DEFAULT NULL,
  `date_suppression` datetime(6) DEFAULT NULL,
  `etat_validation` tinyint(1) NOT NULL,
  `etat_suppression` tinyint(1) NOT NULL,
  `profil_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `player_historiquenotification_profil_id_71089ed1` (`profil_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Structure de la table `player_observation`
--

DROP TABLE IF EXISTS `player_observation`;
CREATE TABLE IF NOT EXISTS `player_observation` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `observation` longtext DEFAULT NULL,
  `date_creation` datetime(6) NOT NULL,
  `date_modification` datetime(6) DEFAULT NULL,
  `date_validation` datetime(6) DEFAULT NULL,
  `date_suppression` datetime(6) DEFAULT NULL,
  `etat_validation` tinyint(1) NOT NULL,
  `etat_suppression` tinyint(1) NOT NULL,
  `modifie_par_id` int(11) DEFAULT NULL,
  `participation_id` bigint(20) DEFAULT NULL,
  `partie_id` bigint(20) DEFAULT NULL,
  `profil_id` bigint(20) DEFAULT NULL,
  `transaction_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `player_observation_modifie_par_id_1cc56eb4` (`modifie_par_id`),
  KEY `player_observation_participation_id_46ad4c0a` (`participation_id`),
  KEY `player_observation_partie_id_6e58f162` (`partie_id`),
  KEY `player_observation_profil_id_7ae47852` (`profil_id`),
  KEY `player_observation_transaction_id_23506cc1` (`transaction_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Structure de la table `player_participation`
--

DROP TABLE IF EXISTS `player_participation`;
CREATE TABLE IF NOT EXISTS `player_participation` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `date_creation` datetime(6) NOT NULL,
  `date_modification` datetime(6) DEFAULT NULL,
  `date_validation` datetime(6) DEFAULT NULL,
  `date_suppression` datetime(6) DEFAULT NULL,
  `etat_validation` tinyint(1) NOT NULL,
  `etat_suppression` tinyint(1) NOT NULL,
  `date_demarrage` datetime(6) DEFAULT NULL,
  `date_fin` datetime(6) DEFAULT NULL,
  `etat_demarrage` tinyint(1) NOT NULL,
  `etat_fin` tinyint(1) NOT NULL,
  `etat_exclusion` tinyint(1) NOT NULL,
  `etat_victoire` tinyint(1) NOT NULL,
  `partie_id` bigint(20) DEFAULT NULL,
  `profil_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `player_participation_partie_id_5919d264` (`partie_id`),
  KEY `player_participation_profil_id_944a5120` (`profil_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Structure de la table `player_partie`
--

DROP TABLE IF EXISTS `player_partie`;
CREATE TABLE IF NOT EXISTS `player_partie` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `code` varchar(25) NOT NULL,
  `nombre_participants` int(10) UNSIGNED NOT NULL CHECK (`nombre_participants` >= 0),
  `montant_mise` decimal(10,2) DEFAULT NULL,
  `montant_cagnotte` decimal(10,2) DEFAULT NULL,
  `montant_commission` decimal(10,2) DEFAULT NULL,
  `visibilite` varchar(20) DEFAULT NULL,
  `delai_tour` int(10) UNSIGNED DEFAULT NULL CHECK (`delai_tour` >= 0),
  `date_creation` datetime(6) NOT NULL,
  `date_modification` datetime(6) DEFAULT NULL,
  `date_validation` datetime(6) DEFAULT NULL,
  `date_suppression` datetime(6) DEFAULT NULL,
  `etat_validation` tinyint(1) NOT NULL,
  `etat_suppression` tinyint(1) NOT NULL,
  `date_demarrage` datetime(6) DEFAULT NULL,
  `date_fin` datetime(6) DEFAULT NULL,
  `etat_demarrage` tinyint(1) NOT NULL,
  `etat_fin` tinyint(1) NOT NULL,
  `config_id` bigint(20) DEFAULT NULL,
  `mise_id` bigint(20) DEFAULT NULL,
  `taux_comission_id` bigint(20) DEFAULT NULL,
  `organise_par_id` bigint(20) DEFAULT NULL,
  `vainqueur_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  KEY `player_partie_config_id_b3d61d99` (`config_id`),
  KEY `player_partie_mise_id_5166729d` (`mise_id`),
  KEY `player_partie_taux_comission_id_e6dda658` (`taux_comission_id`),
  KEY `player_partie_organise_par_id_527f7954` (`organise_par_id`),
  KEY `player_partie_vainqueur_id_ddc77046` (`vainqueur_id`)
) ENGINE=MyISAM AUTO_INCREMENT=15 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Déchargement des données de la table `player_partie`
--

INSERT INTO `player_partie` (`id`, `code`, `nombre_participants`, `montant_mise`, `montant_cagnotte`, `montant_commission`, `visibilite`, `delai_tour`, `date_creation`, `date_modification`, `date_validation`, `date_suppression`, `etat_validation`, `etat_suppression`, `date_demarrage`, `date_fin`, `etat_demarrage`, `etat_fin`, `config_id`, `mise_id`, `taux_comission_id`, `organise_par_id`, `vainqueur_id`) VALUES
(1, '24092024220721941481', 3, 500.00, 1125.00, 375.00, 'Public', NULL, '2024-09-24 22:07:21.941481', '2024-09-24 22:07:21.941481', NULL, NULL, 1, 0, NULL, NULL, 0, 0, NULL, 1, 1, NULL, NULL),
(2, '24092024220721954118', 4, 500.00, 1500.00, 500.00, 'Public', NULL, '2024-09-24 22:07:21.954118', '2024-09-24 22:07:21.954118', NULL, NULL, 1, 0, NULL, NULL, 0, 0, NULL, 1, 1, NULL, NULL),
(3, '24092024220721966298', 2, 1000.00, 1500.00, 500.00, 'Public', NULL, '2024-09-24 22:07:21.966298', '2024-09-24 22:07:21.966298', NULL, NULL, 1, 0, NULL, NULL, 0, 0, NULL, 2, 1, NULL, NULL),
(4, '24092024220721971312', 3, 1000.00, 2250.00, 750.00, 'Public', NULL, '2024-09-24 22:07:21.971312', '2024-09-24 22:07:21.971312', NULL, NULL, 1, 0, NULL, NULL, 0, 0, NULL, 2, 1, NULL, NULL),
(5, '24092024220721991104', 4, 1000.00, 3000.00, 1000.00, 'Public', NULL, '2024-09-24 22:07:21.991104', '2024-09-24 22:07:21.991104', NULL, NULL, 1, 0, NULL, NULL, 0, 0, NULL, 2, 1, NULL, NULL),
(6, '24092024220722001137', 2, 2000.00, 3000.00, 1000.00, 'Public', NULL, '2024-09-24 22:07:22.001137', '2024-09-24 22:07:22.001137', NULL, NULL, 1, 0, NULL, NULL, 0, 0, NULL, 3, 1, NULL, NULL),
(7, '24092024220722011294', 3, 2000.00, 4500.00, 1500.00, 'Public', NULL, '2024-09-24 22:07:22.011294', '2024-09-24 22:07:22.011294', NULL, NULL, 1, 0, NULL, NULL, 0, 0, NULL, 3, 1, NULL, NULL),
(8, '24092024220722027603', 4, 2000.00, 6000.00, 2000.00, 'Public', NULL, '2024-09-24 22:07:22.027603', '2024-09-24 22:07:22.027603', NULL, NULL, 1, 0, NULL, NULL, 0, 0, NULL, 3, 1, NULL, NULL),
(9, '24092024220722039155', 2, 5000.00, 7500.00, 2500.00, 'Public', NULL, '2024-09-24 22:07:22.039155', '2024-09-24 22:07:22.039155', NULL, NULL, 1, 0, NULL, NULL, 0, 0, NULL, 4, 1, NULL, NULL),
(10, '24092024220722051062', 3, 5000.00, 11250.00, 3750.00, 'Public', NULL, '2024-09-24 22:07:22.051062', '2024-09-24 22:07:22.051062', NULL, NULL, 1, 0, NULL, NULL, 0, 0, NULL, 4, 1, NULL, NULL),
(11, '24092024220722061140', 4, 5000.00, 15000.00, 5000.00, 'Public', NULL, '2024-09-24 22:07:22.061140', '2024-09-24 22:07:22.061140', NULL, NULL, 1, 0, NULL, NULL, 0, 0, NULL, 4, 1, NULL, NULL),
(12, '24092024220722071520', 2, 10000.00, 15000.00, 5000.00, 'Public', NULL, '2024-09-24 22:07:22.071520', '2024-09-24 22:07:22.071520', NULL, NULL, 1, 0, NULL, NULL, 0, 0, NULL, 5, 1, NULL, NULL),
(13, '24092024220722083514', 3, 10000.00, 22500.00, 7500.00, 'Public', NULL, '2024-09-24 22:07:22.083514', '2024-09-24 22:07:22.083514', NULL, NULL, 1, 0, NULL, NULL, 0, 0, NULL, 5, 1, NULL, NULL),
(14, '24092024220722099386', 4, 10000.00, 30000.00, 10000.00, 'Public', NULL, '2024-09-24 22:07:22.099386', '2024-09-24 22:07:22.099386', NULL, NULL, 1, 0, NULL, NULL, 0, 0, NULL, 5, 1, NULL, NULL);

-- --------------------------------------------------------

--
-- Structure de la table `player_profil`
--

DROP TABLE IF EXISTS `player_profil`;
CREATE TABLE IF NOT EXISTS `player_profil` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `id_facebook` varchar(25) NOT NULL,
  `nom` varchar(255) DEFAULT NULL,
  `prenom` varchar(255) DEFAULT NULL,
  `genre` varchar(20) DEFAULT NULL,
  `contact` varchar(128) DEFAULT NULL,
  `contact_retrait` varchar(128) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `photo` varchar(100) DEFAULT NULL,
  `code` varchar(25) NOT NULL,
  `code_invite_par` varchar(25) DEFAULT NULL,
  `date_creation` datetime(6) NOT NULL,
  `date_modification` datetime(6) DEFAULT NULL,
  `date_validation` datetime(6) DEFAULT NULL,
  `date_suppression` datetime(6) DEFAULT NULL,
  `etat_validation` tinyint(1) NOT NULL,
  `etat_suppression` tinyint(1) NOT NULL,
  `invite_par_id` bigint(20) DEFAULT NULL,
  `modifie_par_id` int(11) DEFAULT NULL,
  `pays_residence_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_facebook` (`id_facebook`),
  UNIQUE KEY `code` (`code`),
  UNIQUE KEY `user_id` (`user_id`),
  UNIQUE KEY `email` (`email`),
  KEY `player_profil_invite_par_id_8c4bad79_fk_player_profil_id` (`invite_par_id`),
  KEY `player_profil_modifie_par_id_d1f6287d_fk_auth_user_id` (`modifie_par_id`),
  KEY `player_profil_pays_residence_id_32c7580b_fk_cities_li` (`pays_residence_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `player_profil`
--

INSERT INTO `player_profil` (`id`, `id_facebook`, `nom`, `prenom`, `genre`, `contact`, `contact_retrait`, `email`, `photo`, `code`, `code_invite_par`, `date_creation`, `date_modification`, `date_validation`, `date_suppression`, `etat_validation`, `etat_suppression`, `invite_par_id`, `modifie_par_id`, `pays_residence_id`, `user_id`) VALUES
(1, '8982187541826015', 'Phenoom', 'Amos', NULL, NULL, NULL, 'amorosomai@yahoo.fr', '', 'U24ERJL0928', NULL, '2024-09-28 20:36:12.286536', '2024-09-28 20:36:12.286563', NULL, NULL, 1, 0, NULL, NULL, NULL, 1);

-- --------------------------------------------------------

--
-- Structure de la table `player_transaction`
--

DROP TABLE IF EXISTS `player_transaction`;
CREATE TABLE IF NOT EXISTS `player_transaction` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `code` varchar(25) NOT NULL,
  `type` varchar(20) DEFAULT NULL,
  `montant` decimal(10,2) DEFAULT NULL,
  `frais_genere` decimal(10,2) DEFAULT NULL,
  `depot` decimal(10,2) DEFAULT NULL,
  `retrait` decimal(10,2) DEFAULT NULL,
  `mise` decimal(10,2) DEFAULT NULL,
  `gain` decimal(10,2) DEFAULT NULL,
  `description` varchar(225) NOT NULL,
  `contact_transaction` varchar(225) NOT NULL,
  `operateur` varchar(225) NOT NULL,
  `type_api` varchar(225) NOT NULL,
  `date_creation` datetime(6) NOT NULL,
  `date_modification` datetime(6) DEFAULT NULL,
  `date_validation` datetime(6) DEFAULT NULL,
  `date_suppression` datetime(6) DEFAULT NULL,
  `etat_validation` tinyint(1) NOT NULL,
  `etat_suppression` tinyint(1) NOT NULL,
  `config_id` bigint(20) DEFAULT NULL,
  `partie_id` bigint(20) DEFAULT NULL,
  `profil_id` bigint(20) DEFAULT NULL,
  `taux_frais_genere_id` bigint(20) DEFAULT NULL,
  `valide_par_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  UNIQUE KEY `description` (`description`),
  UNIQUE KEY `contact_transaction` (`contact_transaction`),
  UNIQUE KEY `operateur` (`operateur`),
  UNIQUE KEY `type_api` (`type_api`),
  KEY `player_transaction_config_id_c0780b80` (`config_id`),
  KEY `player_transaction_partie_id_d75c0b7c` (`partie_id`),
  KEY `player_transaction_profil_id_ed19262c` (`profil_id`),
  KEY `player_transaction_taux_frais_genere_id_fa45baab` (`taux_frais_genere_id`),
  KEY `player_transaction_valide_par_id_fb63c5ba` (`valide_par_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Structure de la table `socialaccount_socialaccount`
--

DROP TABLE IF EXISTS `socialaccount_socialaccount`;
CREATE TABLE IF NOT EXISTS `socialaccount_socialaccount` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `provider` varchar(200) NOT NULL,
  `uid` varchar(191) NOT NULL,
  `last_login` datetime(6) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `extra_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`extra_data`)),
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `socialaccount_socialaccount_provider_uid_fc810c6e_uniq` (`provider`,`uid`),
  KEY `socialaccount_socialaccount_user_id_8146e70c_fk_auth_user_id` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `socialaccount_socialaccount`
--

INSERT INTO `socialaccount_socialaccount` (`id`, `provider`, `uid`, `last_login`, `date_joined`, `extra_data`, `user_id`) VALUES
(1, 'facebook', '8982187541826015', '2024-09-28 20:36:12.142550', '2024-09-26 23:09:44.603745', '{\"id\": \"8982187541826015\", \"email\": \"amorosomai@yahoo.fr\", \"name\": \"Amos Phenoom\", \"first_name\": \"Amos\", \"last_name\": \"Phenoom\"}', 1);

-- --------------------------------------------------------

--
-- Structure de la table `socialaccount_socialapp`
--

DROP TABLE IF EXISTS `socialaccount_socialapp`;
CREATE TABLE IF NOT EXISTS `socialaccount_socialapp` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `provider` varchar(30) NOT NULL,
  `name` varchar(40) NOT NULL,
  `client_id` varchar(191) NOT NULL,
  `secret` varchar(191) NOT NULL,
  `key` varchar(191) NOT NULL,
  `provider_id` varchar(200) NOT NULL,
  `settings` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`settings`)),
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Structure de la table `socialaccount_socialtoken`
--

DROP TABLE IF EXISTS `socialaccount_socialtoken`;
CREATE TABLE IF NOT EXISTS `socialaccount_socialtoken` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `token` longtext NOT NULL,
  `token_secret` longtext NOT NULL,
  `expires_at` datetime(6) DEFAULT NULL,
  `account_id` int(11) NOT NULL,
  `app_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `socialaccount_socialtoken_app_id_account_id_fca4e0ac_uniq` (`app_id`,`account_id`),
  KEY `socialaccount_socialtoken_account_id_951f210e` (`account_id`),
  KEY `socialaccount_socialtoken_app_id_636a42d7` (`app_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `account_emailaddress`
--
ALTER TABLE `account_emailaddress`
  ADD CONSTRAINT `account_emailaddress_user_id_2c513194_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
