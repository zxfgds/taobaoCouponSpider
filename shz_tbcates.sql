/*
Navicat MySQL Data Transfer

Source Server         : 淘宝客
Source Server Version : 50718
Source Host           : 47.104.154.163:3306
Source Database       : taobaoke

Target Server Type    : MYSQL
Target Server Version : 50718
File Encoding         : 65001

Date: 2018-04-21 14:36:19
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for shz_tbcates
-- ----------------------------
DROP TABLE IF EXISTS `shz_tbcates`;
CREATE TABLE `shz_tbcates` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `catid` int(11) unsigned NOT NULL,
  `name` varchar(255) DEFAULT NULL COMMENT '类目名称',
  `keywords` varchar(255) DEFAULT NULL,
  `start_price` int(11) DEFAULT NULL,
  `end_price` int(11) DEFAULT NULL,
  `step_size` int(11) unsigned DEFAULT NULL COMMENT '价格步长',
  `status` tinyint(2) unsigned DEFAULT '0' COMMENT '0不采集 ;1采集',
  PRIMARY KEY (`id`,`catid`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;
SET FOREIGN_KEY_CHECKS=1;
