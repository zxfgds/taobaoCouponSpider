/*
Navicat MySQL Data Transfer

Source Server         : 淘宝客
Source Server Version : 50718
Source Host           : 47.104.154.163:3306
Source Database       : taobaoke

Target Server Type    : MYSQL
Target Server Version : 50718
File Encoding         : 65001

Date: 2018-04-21 14:36:09
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for shz_appkey
-- ----------------------------
DROP TABLE IF EXISTS `shz_appkey`;
CREATE TABLE `shz_appkey` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `key` varchar(255) DEFAULT NULL,
  `secret` varchar(255) DEFAULT NULL,
  `adzoneid` varchar(255) DEFAULT NULL,
  `ban_time` int(10) unsigned DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4;
SET FOREIGN_KEY_CHECKS=1;
