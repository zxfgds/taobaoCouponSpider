/*
Navicat MySQL Data Transfer

Source Server         : 淘宝客
Source Server Version : 50718
Source Host           : 47.104.154.163:3306
Source Database       : taobaoke

Target Server Type    : MYSQL
Target Server Version : 50718
File Encoding         : 65001

Date: 2018-04-21 14:36:26
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for shz_item_info
-- ----------------------------
DROP TABLE IF EXISTS `shz_item_info`;
CREATE TABLE `shz_item_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `num_iid` varchar(20) NOT NULL,
  `title` varchar(128) DEFAULT NULL COMMENT '商品标题',
  `pict_url` varchar(255) DEFAULT NULL COMMENT '商品图片',
  `small_images` varchar(1500) DEFAULT '[]' COMMENT '商品主图',
  `zk_final_price` decimal(11,2) DEFAULT NULL COMMENT '淘宝天猫价格',
  `short_title` varchar(255) DEFAULT NULL,
  `user_type` int(11) unsigned DEFAULT NULL COMMENT '店铺类型0淘宝  1 天猫',
  `seller_id` bigint(20) DEFAULT '0' COMMENT '卖家id',
  `volume` bigint(20) DEFAULT '0' COMMENT '本月销量',
  `own_cat_id` varchar(256) DEFAULT '' COMMENT '本地自定义分类ID',
  `commission_type` varchar(255) DEFAULT NULL COMMENT 'MKT表示营销计划，SP表示定向计划，COMMON表示通用计划',
  `coupon_end_time` varchar(20) DEFAULT NULL COMMENT '优惠券起始时间',
  `coupon_start_time` varchar(20) DEFAULT NULL COMMENT '优惠券结束时间',
  `coupon_id` varchar(64) DEFAULT NULL COMMENT '券ID',
  `coupon_remain_count` int(11) DEFAULT NULL COMMENT '剩余优惠券数量',
  `coupon_start_fee` int(11) unsigned DEFAULT NULL COMMENT '优惠券适用jiage',
  `catemain` int(11) unsigned DEFAULT NULL COMMENT '淘宝根分类',
  `category` int(11) DEFAULT NULL COMMENT '淘宝分类ID',
  `coupon_info` varchar(128) DEFAULT NULL COMMENT '优惠券信息',
  `queqiao` decimal(11,0) DEFAULT NULL COMMENT '高佣比例',
  `commission_rate` decimal(11,2) DEFAULT NULL COMMENT '佣金比例',
  `coupon_total_count` int(11) DEFAULT NULL COMMENT '优惠券总数',
  `coupon_value` int(11) DEFAULT '0' COMMENT '优惠券金额',
  `tao_ke_price` decimal(11,2) DEFAULT '0.00' COMMENT '淘宝客价格(扣除优惠券后的价格)',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `commission` float(11,2) DEFAULT '0.00' COMMENT '佣金',
  `updated_at` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `keyId` int(11) unsigned DEFAULT NULL,
  `free_shipment` tinyint(2) unsigned DEFAULT '0' COMMENT '1:包邮;0:不包邮',
  `qqhd` tinyint(2) unsigned DEFAULT '0' COMMENT '高佣 0 否 ;1 是;',
  `jyj` tinyint(2) unsigned DEFAULT '0' COMMENT '极有家频道 :0 否 1 是',
  `9k9` tinyint(2) unsigned DEFAULT '0' COMMENT '9块9',
  `20k` tinyint(2) unsigned DEFAULT '0' COMMENT '20块封顶',
  `provcity` varchar(255) DEFAULT NULL COMMENT '发货地',
  `tk_total_sales` int(11) unsigned DEFAULT NULL COMMENT '推广数量',
  `item_url` varchar(255) DEFAULT NULL COMMENT 'wangzhi',
  `include_mkt` tinyint(2) unsigned DEFAULT '0' COMMENT '定向计划',
  `include_dxjh` tinyint(2) unsigned DEFAULT '0' COMMENT '营销计划',
  `tk_total_commi` float(11,2) unsigned DEFAULT '0.00' COMMENT '30天支出佣金',
  `shop_title` varchar(255) DEFAULT NULL COMMENT '店铺名称',
  PRIMARY KEY (`id`,`num_iid`),
  UNIQUE KEY `num_iid` (`num_iid`) USING BTREE,
  KEY `category` (`category`),
  KEY `title` (`title`)
) ENGINE=InnoDB AUTO_INCREMENT=1101270 DEFAULT CHARSET=utf8;
SET FOREIGN_KEY_CHECKS=1;
